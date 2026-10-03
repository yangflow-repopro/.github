# Legal pages

An app is licensed under terms that are also its license agreement. The text exists once in English as the
repository's `LICENSE` and is published, translated, on the product website at `/terms`. A privacy policy
(`/privacy`) and a refund policy (`/refund`) live on the website only.

## One source per fact

Every number or promise that appears in legal text (what the free plan includes, how many Macs a key covers,
how long the offline grace is, what is sent to whom, the refund window) has exactly one place where it is
written as a fact: the table "Facts that must match the code" in the app's `docs/legal.md`. For each fact the
table gives the fact, the code symbol that implements it, the website key that states it, and the check that
compares them. The website's `scripts/check_facts.py` verifies that the numbers agree across all nine
languages and with that table.

## The app only links to the website

The app links to `/terms`, `/privacy`, `/refund` and `/changelog` on its website, by those paths only. It
does not embed or duplicate the policies. The website only links to the app repository by stable path
(`docs/legal.md#...`), never by section number.

## Skeletons

`LICENSE` (terms of service) has these numbered sections, in this order: License · Free plan and Pro ·
License key · Activation and verification · Your data and credentials · Restrictions · Updates ·
Third-party components · Purchases and refunds · Intellectual property · Termination · Disclaimer · Limitation
of liability · Changes. The section "Your data and credentials" is the product's slot: it says what the
product touches on the user's behalf. Everything else is the same wording pattern in every product.

`/privacy` and `/refund` follow the section lists in `templates/legal.md`.

## Wording that is always the same

- Company name in legal text: `yangflow` (copyright line: `Copyright (c) <year> yangflow. All rights reserved.`).
- Support address: `support@<domain>`, the same on the website footer, in `SECURITY.md` and in the legal text.
- Payments: processed by Dodo Payments as merchant of record; the terms say so once, in "Purchases and refunds".
- Translations: every non-English legal page and FAQ opens with a notice that the English text is the
  reference. This includes Chinese.
- "Last updated" is a month and year, changed whenever the text changes.
