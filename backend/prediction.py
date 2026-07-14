import io
import os
import logging
import numpy as np
from PIL import Image
from backend.cost import estimate_repair_cost, estimate_repair_time

logger = logging.getLogger(__name__)

CLASSES = ["Cracks", "Patch", "Potholes", "Surface Defects"]

CLASS_SEVERITY = {
    "Cracks": 0.50,
    "Patch": 0.25,
    "Potholes": 0.75,
    "Surface Defects": 0.60,
}

_models = None
_transform = None
MODEL_STATUS = "unavailable"  # "loading", "loaded", "unavailable", "error"


def _load_models():
    global _models, _transform, MODEL_STATUS
    if _models is not None:
        logger.info("_load_models: models already loaded, returning cached")
        return _models, _transform

    MODEL_STATUS = "loading"
    logger.info("_load_models: starting model loading")

    try:
        from torchvision import transforms
        from src.model import get_model
        from src.config import Config
        import torch
        logger.info("Imports OK: torch=%s, device=%s", torch.__version__, Config.DEVICE)
    except ImportError as e:
        logger.warning("Import FAILED: %s", e, exc_info=True)
        MODEL_STATUS = "unavailable"
        return None, None

    _transform = transforms.Compose([
        transforms.Resize((Config.IMAGE_SIZE, Config.IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    logger.info("Transform ready: size=%s", Config.IMAGE_SIZE)

    _models = []
    model_names = Config.ENSEMBLE_MODELS if len(Config.ENSEMBLE_MODELS) > 0 else [Config.MODEL_NAME]
    logger.info("Model names to load: %s", model_names)

    for name in model_names:
        model_path = Config.get_model_path(model_name=name)
        logger.info("Processing model='%s': path='%s', exists=%s", name, model_path, os.path.exists(model_path))

        if not os.path.exists(model_path):
            logger.info("Path not found. models/ dir contents: %s", os.listdir("models") if os.path.isdir("models") else "DIR NOT FOUND")
            try:
                from huggingface_hub import hf_hub_download
                os.makedirs("models", exist_ok=True)
                logger.info("Starting hf_hub_download(repo_id='amruthjakku/surface-crack-detection-model', filename='%s_best.pth', local_dir='models')", name)
                downloaded = hf_hub_download(
                    repo_id="amruthjakku/surface-crack-detection-model",
                    filename=f"{name}_best.pth",
                    local_dir="models"
                )
                file_size = os.path.getsize(downloaded) if os.path.exists(downloaded) else -1
                logger.info("Download SUCCESS: path='%s', size=%d bytes", downloaded, file_size)
                model_path = downloaded
            except Exception as e:
                logger.warning("Download FAILED: %s", e, exc_info=True)
                import pathlib
                cache_dir = pathlib.Path.home() / ".cache" / "huggingface" / "hub"
                if cache_dir.is_dir():
                    logger.warning("HF cache dir exists at %s, contents: %s", cache_dir, os.listdir(str(cache_dir)))
                else:
                    logger.warning("HF cache dir %s does not exist", cache_dir)

        if os.path.exists(model_path):
            try:
                logger.info("Loading model from '%s'", model_path)
                m = get_model(model_name=name, num_classes=Config.NUM_CLASSES, pretrained=False)
                data = torch.load(model_path, map_location=Config.DEVICE)
                if isinstance(data, dict):
                    logger.info("Checkpoint keys: %s", list(data.keys()))
                    if "model_state_dict" in data or "state_dict" in data:
                        data = data.get("model_state_dict") or data["state_dict"]
                        logger.info("Extracted state_dict from checkpoint wrapper")
                else:
                    logger.info("Checkpoint is a bare tensor/list, not a dict")
                m.load_state_dict(data)
                m.to(Config.DEVICE)
                m.eval()
                num_params = sum(p.numel() for p in m.parameters())
                logger.info("Model '%s' loaded OK: %d parameters, device=%s", name, num_params, Config.DEVICE)
                _models.append(m)
            except Exception as e:
                logger.warning("Model load FAILED for '%s': %s", name, e, exc_info=True)

    if len(_models) > 0:
        MODEL_STATUS = "loaded"
        logger.info("_load_models: done. Loaded %d model(s), status=%s", len(_models), MODEL_STATUS)
    else:
        MODEL_STATUS = "unavailable"
        _models = None
        logger.warning("_load_models: done. No models loaded, status=unavailable")
    return _models, _transform


def _tta_predict(models, input_tensor):
    """Run inference with Test-Time Augmentation and return averaged probabilities."""
    from src.config import Config
    import torch
    from torchvision import transforms as T

    all_probs = []
    # Base prediction
    with torch.no_grad():
        for m in models:
            outputs = m(input_tensor)
            probs = torch.softmax(outputs, dim=1).squeeze(0).cpu().numpy()
            all_probs.append(probs)

    if not Config.TTA_ENABLED:
        return np.mean(all_probs, axis=0)

    # Test-time augmentations
    tta_transforms = [
        lambda x: x,
        lambda x: T.functional.hflip(x),
        lambda x: T.functional.vflip(x),
        lambda x: T.functional.rotate(x, 90),
        lambda x: T.functional.rotate(x, 180),
        lambda x: T.functional.rotate(x, 270),
    ]
    for aug in tta_transforms[1:]:
        aug_tensor = aug(input_tensor)
        with torch.no_grad():
            for m in models:
                outputs = m(aug_tensor)
                probs = torch.softmax(outputs, dim=1).squeeze(0).cpu().numpy()
                all_probs.append(probs)

    return np.mean(all_probs, axis=0)


def predict_image(image_bytes: bytes, filename: str = "upload.jpg") -> dict:
    models, transform = _load_models()

    if models is not None:
        try:
            pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
            import torch
            input_tensor = transform(pil_image).unsqueeze(0).to("cpu")

            avg_probs = _tta_predict(models, input_tensor)
            pred_idx = int(np.argmax(avg_probs))
            confidence = float(avg_probs[pred_idx])
            predicted_class = CLASSES[pred_idx]
        except Exception:
            predicted_class = "N/A"
            confidence = 0.0
            avg_probs = np.array([0.25, 0.25, 0.25, 0.25])
    else:
        predicted_class = "N/A"
        confidence = 0.0
        avg_probs = np.array([0.25, 0.25, 0.25, 0.25])

    base_sev = CLASS_SEVERITY.get(predicted_class, 0.5)
    severity_score = round(min(base_sev * (0.5 + 0.5 * confidence), 1.0), 3)

    # 3-tier severity: Low / Medium / High
    if severity_score < 0.35:
        severity_label = "Low"
    elif severity_score < 0.65:
        severity_label = "Medium"
    else:
        severity_label = "High"

    result = {
        "success": True,
        "predicted_class": predicted_class,
        "confidence": round(confidence, 4),
        "class_probabilities": {
            cls: round(float(p), 4) for cls, p in zip(CLASSES, avg_probs)
        },
        "severity_score": severity_score,
        "severity_label": severity_label,
    }

    # Only estimate cost/time if we have a real prediction
    if predicted_class in CLASS_SEVERITY:
        cost_estimate = estimate_repair_cost(predicted_class, severity_label, confidence)
        time_estimate = estimate_repair_time(predicted_class, severity_label, confidence)
        result["repair_cost"] = cost_estimate
        result["repair_time"] = time_estimate
    else:
        result["repair_cost"] = None
        result["repair_time"] = None

    return result