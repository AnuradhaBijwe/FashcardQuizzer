# Concept 1: Context Gap Prevention

**Exercise Goal**: Use structured prompts to prevent AI from losing existing functionality when adding new features.

**Prompt 1** (Structured Approach):
```xml
<task>
Add fraud detection to payment processing function
</task>

<requirements>
- Add fraud check before payment validation using detect_fraud(user_id, amount, payment_method)
- Raise FraudError if fraud detected
- PRESERVE ALL EXISTING FUNCTIONALITY:
  * Payment validation
  * Account balance updates
  * Confirmation email sending
  * Analytics logging
  * All error handling
</requirements>

<constraints>
- No changes to existing error handling patterns
- Maintain same function signature
- Fraud detection must happen BEFORE any payment processing
</constraints>
```

**Prompt 2** (Verify Completeness):
```xml
<task>
Verify this updated payment processor maintains all functionality
</task>

<verification_checklist>
- [ ] Fraud detection added before payment validation
- [ ] Payment validation still occurs
- [ ] Account balance updates after successful payment
- [ ] Confirmation email sent
- [ ] Analytics logged
- [ ] All error handling preserved
</verification_checklist>
```