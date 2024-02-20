# Turnstile

[Cloudflare Turnstile · Cloudflare Turnstile docs](https://developers.cloudflare.com/turnstile/)

## Example
[cloudflare / turnstile-demo-workers](https://github.com/cloudflare/turnstile-demo-workers)

## [Widget types](https://developers.cloudflare.com/turnstile/reference/widget-types/)

|     | Managed | Non-Interactive | Invisible |
| --- | --- | --- | --- |
| interactive? | yes | no | no |
| visible? | yes | yes | no |

各々、下記を持つ
- mode
- label
- sitekey
  - サイト上でTurnstile起動に必要
- secret key
  - widgetの応答を検証する際、Turnstile serverとのやり取りで必要


## Prepare

### Getting a sitekey and secret key

sitekeyとsecret keyはwidgetごとに必要。

|     | sitekey | secret key |
| --- | --- | --- |
| needs per widget? | yes | yes |
| public? | yes | no |

