# Security Policy

## Scope

This policy covers the public static website at https://jixsaw79.github.io/Z-Society/ and this repository:
https://github.com/Jixsaw79/Z-Society

## Reporting a vulnerability

Report suspected security issues privately by emailing **shadmanibtesham79@gmail.com**.

Include:

- the affected URL or file
- a concise description
- steps to reproduce
- the potential impact

Do not send passwords, private keys, or unrelated personal data.

Please do not open a public issue for an unpatched vulnerability. This is a personal team site; there is no bug bounty and no guaranteed response time.

## Safe testing

- Test only this website and repository.
- Do not attempt denial-of-service, spam, social engineering, or account compromise.
- Do not access or modify data that is not yours.
- Stop if you encounter information that appears private.

## Security design

This is a **static, zero-JavaScript** GitHub Pages site.

Controls in the HTML:

- `script-src 'none'` — no scripts
- `object-src 'none'` — no plugins
- `connect-src 'none'` — no page-initiated network requests
- `form-action 'none'` — no forms
- `frame-src 'none'` / `child-src 'none'` — no frames
- `style-src-attr 'none'` — no inline style attributes from markup injection paths we control
- `upgrade-insecure-requests`
- No third-party script, analytics, or font CDNs
- External links use `rel="noopener noreferrer"`

## Limitations

GitHub Pages does not let this repo set arbitrary HTTP response headers. HSTS, Permissions-Policy, and `frame-ancestors` depend on the host. Meta CSP is defense in depth, not a substitute for protecting the GitHub account that publishes the site.

Protect the GitHub account with a strong unique password and two-factor authentication. Never commit secrets, tokens, or private flags to this repository.
