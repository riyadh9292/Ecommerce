# checkout process

1. Cart -> checkout view
  ?
  - Login or enter email
  -shipping address
  -billing Info
    -billing address
    -credit card/payment

2. billing app/component
  -billing profile
    -user/email(guest email)
    -generate payment processor token(Stripe or Braintee)

3. Order/invoices Component
  -connecting the billing profile
  -shipping/billing aaddress
  -cart
  -status--shipped?cancelled?
