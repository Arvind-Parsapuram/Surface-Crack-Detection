# Implementation Plan

[Overview]
Implement full path-based SPA routing for all pages with deep-link support, replacing the broken hash-based and middleware-rewritten routing.

The current routing system has two fundamental problems. First, the `SPAMiddleware` in `app.py` rewrites `/login`, `/register`, and `/forgot` to `/` at the FastAPI level before the JavaScript can read the pathname, making the JS `checkInitialPath()` function useless. Second, the main app pages (Dashboard, Predict, User, About) only use hash-based routing (`#/dashboard`, `#/predict`, etc.) with no real URL paths, preventing deep-linking and breaking browser back/forward navigation. The solution is to remove the middleware, add a catch-all FastAPI route, and implement proper path-based SPA routing entirely in JavaScript using `history.pushState` and `popstate` events, with Gradio event handlers that update the URL to match the current page state.

[Types]
No new types, classes, or data structures are needed — the existing string-based state values (`"landing"`, `"login"`, `"register"`, `"forgot"`, `"Dashboard"`, `"Predict"`, `"User"`, `"About Us"`, `"Logout"`) remain unchanged.

The URL path mapping is:

- `/` or ``→`"landing"` (auth landing page)
- `/login` → `"login"` (login form)
- `/register` → `"register"` (registration form)
- `/forgot` → `"forgot"` (forgot password form)
- `/dashboard` → `"Dashboard"` (main dashboard page)
- `/predict` → `"Predict"` (predict page)
- `/user` → `"User"` (user profile page)
- `/about` → `"About Us"` (about page)
- `/logout` → `"Logout"` (logout modal)

[Files]
Three files will be modified; no files will be created or deleted.

- **`app.py`** — Remove `SPAMiddleware` class and its registration. Add a catch-all FastAPI route (`@fastapi_app.api_route("/{path:path}", methods=["GET"])`) that returns the Gradio HTML for any path, ensuring deep-links work without 404 errors.

- **`ui/assembly.py`** — Rewrite the `NAV_JS` JavaScript to:
  1. Remove all hash-based routing logic (`hashchange` listener, `updateHash`, `hashHandler`)
  2. Replace with path-based routing: read `location.pathname` on load, update `location.pathname` via `history.pushState` on navigation
  3. Keep the existing click delegation for auth buttons but update paths instead of hashes
  4. Add a `popstate` listener for browser back/forward
  5. Add a MutationObserver to reset path to `/` after successful login
  6. Remove the `SPAMiddleware`-dependent `checkInitialPath` logic

- **`ui/handlers/navigation.py`** — Update `navigate()` and `do_logout()` to return the URL path as an additional output, so Gradio can trigger a JS-side path update. Add a new `update_path()` function that returns a path string for the Gradio frontend to consume.

[Functions]

**Modified functions:**

1. **`navigate(choice, user)`** in `ui/handlers/navigation.py` — Add a return value for the URL path string. After determining which page is visible, return the corresponding path (e.g., `"/dashboard"`, `"/predict"`, `"/user"`, `"/about"`, `"/logout"`) as an additional element in the return tuple. The existing visibility logic remains unchanged.

2. **`do_logout()`** in `ui/handlers/navigation.py` — Add `"/"` as the final return value to reset the URL path to root after logout.

3. **`cancel_logout()`** in `ui/handlers/navigation.py` — Add `"/dashboard"` as the final return value to restore the dashboard path when cancel is clicked.

**New functions:**

1. **`update_path(path: str) -> str`** in `ui/handlers/navigation.py` — A simple passthrough function that returns the path string. This is used as a Gradio `.then()` callback to update the URL after navigation events. The JavaScript will watch this output and call `history.pushState`.

**Removed functions:**

- None. The `show_login()`, `show_register()`, `show_forgot()` convenience functions remain but are unused — they can be kept for backward compatibility.

[Classes]
No classes will be created, modified, or removed.

[Dependencies]
No new dependencies. The existing `gradio`, `fastapi`, `starlette`, and `uvicorn` packages are sufficient.

[Testing]
Manual testing of all navigation flows:

1. Visit `/` → should show landing page
2. Click "Login" → URL changes to `/login`, login form visible
3. Click "Create Account" → URL changes to `/register`, register form visible
4. Click "Forgot Password?" → URL changes to `/forgot`, forgot password form visible
5. Click "Back to Login" → URL changes to `/login`, login form visible
6. Login with admin credentials → URL changes to `/dashboard`, main app visible
7. Click sidebar "Predict" → URL changes to `/predict`, predict page visible
8. Click sidebar "User" → URL changes to `/user`, user page visible
9. Click sidebar "About Us" → URL changes to `/about`, about page visible
10. Click sidebar "Logout" → URL changes to `/logout`, logout modal visible
11. Cancel logout → URL changes to `/dashboard`, dashboard visible
12. Confirm logout → URL changes to `/`, landing page visible
13. Direct URL entry `/predict` → should show predict page (if authenticated) or redirect to login
14. Browser back/forward buttons → should navigate correctly via `popstate`

[Implementation Order]
Single atomic change — all three files must be modified together since they are interdependent.

1. Modify `app.py` to remove SPAMiddleware and add catch-all route
2. Modify `ui/handlers/navigation.py` to add path return values and `update_path()` function
3. Modify `ui/assembly.py` to rewrite NAV_JS with path-based routing and update Gradio event chains to include path updates
