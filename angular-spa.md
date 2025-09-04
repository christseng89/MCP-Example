# Build a **single “portal” domain** (e.g., `https://portal.xxx.com`) and put all tools **behind path-based reverse proxy routes**

* `https://portal.xxx.com/gitlab/`  → GitLab
* `https://portal.xxx.com/sonarqube/` → SonarQube
* `https://portal.xxx.com/kafka/` → Kafka UI

Then your Angular SPA can either:

1. **Navigate in the same tab** to those paths (no new window), or
2. **Embed them in an `<iframe>`** inside a portal page (works well because they’re now same-origin).

This avoids cross-origin issues you’d hit with `gitlab.xxx.com`, `sonarqube.xxx.com`, etc.

## What you need

### 1) Reverse proxy (Ingress/NGINX/Traefik)

Path-route each app and rewrite cookies to the subpath so they don’t collide.

#### Kubernetes (NGINX Ingress) example

```yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: portal
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
    nginx.ingress.kubernetes.io/use-regex: "true"
    # Make upstream apps aware of their mount path
    nginx.ingress.kubernetes.io/proxy-set-headers: "portal-headers"
    # Rewrite Set-Cookie Path=/ to Path=/gitlab (and similarly for others)
    nginx.ingress.kubernetes.io/proxy-cookie-path: / /gitlab;
spec:
  rules:
  - host: portal.xxx.com
    http:
      paths:
      - path: /gitlab(/|$)(.*)
        pathType: Prefix
        backend:
          service:
            name: gitlab-webservice
            port:
              number: 8080
      - path: /sonarqube(/|$)(.*)
        pathType: Prefix
        backend:
          service:
            name: sonarqube
            port:
              number: 9000
      - path: /kafka(/|$)(.*)
        pathType: Prefix
        backend:
          service:
            name: kafka-ui
            port:
              number: 8080
```

Create the `portal-headers` ConfigMap to pass the mount path to each app (many apps respect these):

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: portal-headers
data:
  X-Forwarded-Prefix: /gitlab
  X-Forwarded-Proto: https
  X-Forwarded-Host: portal.xxx.com
```

(You can also do app-specific Ingresses with their own `proxy-cookie-path` and `X-Forwarded-Prefix`.)

#### Bare NGINX (non-K8s) sketch

```nginx
server {
  server_name portal.xxx.com;
  location ~ ^/gitlab/?(.*)$ {
    proxy_pass http://gitlab:8080/$1;
    proxy_set_header X-Forwarded-Prefix /gitlab;
    proxy_cookie_path / /gitlab;
  }
  location ~ ^/sonarqube/?(.*)$ {
    proxy_pass http://sonarqube:9000/$1;
    proxy_set_header X-Forwarded-Prefix /sonarqube;
    proxy_cookie_path / /sonarqube;
  }
  location ~ ^/kafka/?(.*)$ {
    proxy_pass http://kafka-ui:8080/$1;
    proxy_set_header X-Forwarded-Prefix /kafka;
    proxy_cookie_path / /kafka;
  }
}
```

### 2) App base paths

Configure each app to live under a subpath (names vary by product/version), e.g.:

* **GitLab:** set a “relative URL root” (e.g., `/gitlab`) and ensure assets/callbacks honor it.
* **SonarQube:** set a context/base path so UI/API work under `/sonarqube`.
* **Kafka UI:** set `server.servlet.context-path=/kafka` (Spring-based UIs commonly support this).

(Exact keys differ per version—look for “relative URL”, “context path”, or “base URL” in each app’s docs.)

### 3) Optional: embed inside your Angular portal

Since everything is now same-origin, most apps that use `frame-ancestors 'self'` will iframe fine.

```ts
// apps-page.component.ts
import { Component } from '@angular/core';
@Component({
  selector: 'app-apps',
  template: `
    <div class="shell">
      <header>
        <button (click)="src='/gitlab/'">GitLab</button>
        <button (click)="src='/sonarqube/'">SonarQube</button>
        <button (click)="src='/kafka/'">Kafka UI</button>
      </header>
      <iframe [src]="src" sandbox="allow-scripts allow-forms allow-same-origin"></iframe>
    </div>
  `,
  styles: [`
    .shell { height: 100vh; display:flex; flex-direction:column }
    header { padding: .5rem; border-bottom: 1px solid #ddd }
    iframe { flex:1; width:100%; border:0 }
  `]
})
export class AppsPageComponent {
  src = '/gitlab/';
}
```

If an app still sends blocking headers (e.g., `X-Frame-Options: DENY` or restrictive CSP), adjust that app’s config to allow `frame-ancestors 'self'` or specifically `portal.xxx.com`. As a last resort, you can strip/override headers at the proxy—but prefer fixing them at the app.

### 4) SSO (nice-to-have)

Use a central IdP (Keycloak/Auth0/ADFS via OIDC). Give each app its own OIDC client; users log in once, then hop across `/gitlab`, `/sonarqube`, `/kafka` without re-auth. This keeps you on one domain and one tab.

### 5) Gotchas & tips

* **Cookies:** Always rewrite `Path=/` to the app subpath (`/gitlab`, etc.) to avoid cookie collisions with your portal.
* **Service Workers:** Keeping apps on subpaths prevents third-party service workers from taking over your portal scope.
* **WebSockets/SSE:** Enable HTTP/1.1 + upgrade headers on the proxy for GitLab live features, Kafka streaming UIs, etc.
* **CSP:** If you iframe, set/allow `frame-ancestors 'self' portal.xxx.com`.
* **Performance:** Let proxy cache static assets for each app; keep TLS at the edge with HSTS.

---

## Bottom line

Use a **single portal domain + path-based reverse proxy**. It keeps everything in one origin and one tab, enables SSO, and (if you want) lets your Angular SPA **embed** each tool inside a consistent shell with a shared header and back button—without opening new pages.
