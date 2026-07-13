try:
    from backend import database as db_module
except ImportError:
    db_module = None


def load_prediction_history(user_id, session_history):
    if db_module and hasattr(db_module, "get_user_analyses") and user_id:
        try:
            records = db_module.get_user_analyses(user_id)
            if records:
                return records
        except Exception:
            pass
    return session_history


def save_prediction_record(user_id, record, session_history):
    session_history.insert(0, record)
    if db_module and hasattr(db_module, "save_analysis") and user_id:
        try:
            db_module.save_analysis(user_id, record)
        except Exception:
            pass
    return session_history
