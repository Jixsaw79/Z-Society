# Security Policy

## Scope

This policy covers the public static website at https://jixsaw79.github.io/Z-Society/ and this repository:
https://github.com/Jixsaw79/Z-Society

## Reporting a vulnerability

Report suspected security issues privately by emailing **shadmanibtesham79@gmail.com**.

Include the affected URL or file, a concise description, reproducible steps, and potential impact. Do not send passwords, private keys, or unrelated personal data.

Please do not open a public issue for an unpatched vulnerability. This is a personal team site; there is no bug bounty and no guaranteed response time.

## Safe testing

- Test only this website and repository.
- Do not attempt denial-of-service, spam, social engineering, or account compromise.
- Do not access or modify data that is not yours.
- Stop if you encounter information that appears private.

## Security design

This is a static, zero-JavaScript GitHub Pages site. The HTML uses a restrictive **meta-delivered Content Security Policy**:

- `default-src 'none'` denies resource types unless explicitly allowed.
- `script-src 'none'` disables JavaScript.
- `object-src 'none'` disables plugin content.
- `base-uri 'none'` prevents injected base URLs from changing relative URL resolution.
- `connect-src 'none'` blocks page-initiated fetch/XHR/WebSocket connections.
- `form-action 'none'` blocks form submissions.
- `frame-src 'none'` and `child-src 'none'` block embedded frames and child contexts.
- `img-src 'self' data:` permits only same-origin images and the inline SVG favicon.
- `style-src 'self'` and `style-src-attr 'none'` restrict styles to the local stylesheet.
- `font-src 'self'` disallows remote font providers.
- `upgrade-insecure-requests` upgrades insecure resource requests.

Additional controls:

- No client-side JavaScript, inline event handlers, forms, third-party scripts, analytics, embeds, or remote fonts.
- External links opened in a new tab use `rel="noopener noreferrer"`.
- A repository security audit runs on pushes and pull requests.
- `robots.txt` and `sitemap.xml` are discovery files, not security controls.

## Platform limitations

GitHub Pages does not let this repository configure arbitrary HTTP response headers. A CSP delivered through a meta element is useful defence in depth, but it is not equivalent to an HTTP response-header CSP.

In particular, `frame-ancestors` and other response-header-only protections cannot be reliably enforced through this meta policy. This repository cannot set HSTS, `X-Content-Type-Options`, `Permissions-Policy`, or `X-Frame-Options` response headers. Do not add ineffective meta tags pretending to set those headers.

The site has no login, database, API, server-side form handler, or secrets. Do not add these features without a separate threat model and security review.

## GitHub account and repository hardening

The repository owner should also:

1. Enable two-factor authentication or a passkey on the GitHub account; store recovery codes offline.
2. Review active sessions, authorised OAuth/GitHub Apps, SSH keys, and personal access tokens; revoke anything unused or unfamiliar.
3. Keep the repository's `main` branch protected: require pull requests, require the security-audit status check, require conversation resolution, block force pushes and branch deletion, and do not allow bypass for routine changes.
4. Enable Dependabot alerts and secret-scanning/push-protection features when available for the repository/account.
5. Keep repository write access limited to trusted contributors. Review collaborator access periodically.
6. Never commit credentials, API keys, private flags, challenge files, or tokens. If a secret is exposed, revoke/rotate it immediately; deleting the commit is not enough.

Some GitHub security features depend on account plan and repository eligibility. Verify their actual status in GitHub Settings; this file does not enable them automatically.

## Maintenance

Review this policy and the deployed site periodically. Treat a passing static audit as a basic regression check, not proof that the website is secure or a substitute for a professional security assessment.
