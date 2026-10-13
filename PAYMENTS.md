# Payment-Link Runbook

## Current state

Online payment is deliberately fail-closed. Both values in `checkout-config.js` are blank, the checkout button stays hidden, and email ordering remains available.

The website never collects card numbers, CVC/CVV values, expiration dates, bank details, or Stripe secret keys.

## Products and prices

| Key | Product | Required amount | Currency | Timing |
|---|---|---:|---|---|
| `single` | One 60-minute private C/C++ lesson | $100 | USD | Ongoing |
| `course` | Fourteen 60-minute private C/C++ lessons | $400 | USD | New Year sale, before January 1, 2027 at 12:00 a.m. Pacific |
| `course` after sale | Fourteen 60-minute private C/C++ lessons | $1,000 | USD | At and after January 1, 2027 at 12:00 a.m. Pacific |

The course normally costs $1,000. During the sale it is $400, which is 60% off and $1,000 less than buying fourteen individual $100 lessons.

## Creation procedure

1. Connect the authorized Stripe account.
2. Create or identify one product for the single lesson and one for the fourteen-lesson course.
3. Create fixed USD prices matching the table above.
4. Create Stripe-hosted Payment Links from the exact prices.
5. Do not enable recurring billing, quantity adjustment, customer-set pricing, or unrelated upsells unless separately approved.
6. Keep scheduling outside payment: paying does not reserve a lesson time.
7. Review Stripe tax, refund, cancellation, receipt, and customer-data settings before activation.

## Independent verification

Before placing either public link in `checkout-config.js`, a second review must record:

- Stripe account/business identity;
- product name and description;
- one-time payment mode;
- amount and USD currency;
- no adjustable quantity or customer-set amount;
- live vs. test mode;
- destination host exactly `buy.stripe.com`;
- sale start/end applicability for the course link;
- reviewer identity, timestamp, and evidence location.

A URL-format check cannot prove the provider-side product, amount, currency, tax treatment, or payment status.

## Publication

Only the public Stripe Payment Link may be committed. Never commit API keys, webhook signing secrets, deploy hooks, customer data, dashboard URLs containing credentials, or private evidence.

Update:

```js
window.CHECKOUT_LINKS = Object.freeze({
  single: "https://buy.stripe.com/<verified-single-link>",
  course: "https://buy.stripe.com/<verified-course-link>"
});
```

Then run:

```sh
python tools/validate_site.py
```

The GitHub Actions workflow runs the same validator after a push.

## Sale expiration

At January 1, 2027 at 12:00 a.m. Pacific:

1. Replace the $400 course Payment Link with the independently verified $1,000 course link.
2. Remove expired sale copy from graphics metadata and all Basic HTML pages.
3. Retain the regular $1,000 course price and $400 package savings relative to fourteen individual lessons.
4. Run the validator and publish the exact passing commit.
5. Confirm production serves the same commit SHA.

The validator fails future publication when expired New Year sale copy remains after the recorded deadline.
