# Concept 3: Reliability Risk Assessment

**Exercise Goal**: Identify reliability risks in AI systems and implement robustness safeguards.

**Prompt 1** (Reliability Risk Assessment):
```xml
<task>
Comprehensive reliability risk assessment for Financial Data Processing Pipeline
</task>

<reliability_framework>
Analyze for:

1. Failure Modes:
   - What happens when components fail?
   - Graceful degradation vs catastrophic failure
   - Single points of failure

2. Input Validation:
   - Handling of unexpected inputs
   - Edge cases and boundary conditions
   - Malformed data handling

3. Error Propagation:
   - How errors cascade through system
   - Error recovery mechanisms
   - Logging and alerting

4. Data Quality:
   - Missing data handling
   - Outlier detection
   - Data staleness issues

5. Performance Under Load:
   - Response time guarantees
   - Behavior under high load
   - Resource exhaustion scenarios

6. Safety Criticality:
   - Potential for client harm
   - False positive/negative risks
   - Fail-safe mechanisms
</reliability_framework>

<risk_classification>
For each risk:
- Likelihood: High/Medium/Low
- Impact: Critical/High/Medium/Low
- Safety Criticality: Client safety/System availability/Data integrity
- Mitigation Priority: Immediate/High/Medium/Low
</risk_classification>
```

**Prompt 2** (Implement Reliability Safeguards):
```xml
<role>
Reliability engineer for safety-critical financial systems
</role>

<task>
Add comprehensive reliability safeguards to financial recommendation system
</task>

<reliability_requirements>
<input_validation>
- Validate all client data against finantial ranges
- Reject malformed inputs with clear errors
- Handle missing data explicitly (never guess)
- Check data freshness (no stale data)
- Validate data types and units
</input_validation>

<error_handling>
- Fail-safe defaults (conservative recommendations when uncertain)
- Graceful degradation (reduced functionality vs complete failure)
- Clear error messages for clinicians
- No silent failures
- Comprehensive error logging
</error_handling>

<safety_mechanisms>
- Human-in-the-loop for critical recommendations
- Confidence thresholds (defer to human if low confidence)
- Alert system for anomalous recommendations
- Override mechanism for banks
- Regular calibration against banking outcomes
</safety_mechanisms>

<monitoring>
- Real-time performance metrics
- Error rate tracking
- Response time monitoring
- Recommendation accuracy tracking
- Alert system for degraded performance
</monitoring>

<testing>
- Comprehensive edge case testing
- Failure mode simulation
- Load testing
- Data quality testing
- Financial validation
</testing>
</reliability_requirements>

<constraints>
- Medical device regulatory compliance
- Patient safety is paramount
- No recommendation without sufficient confidence
- Human oversight required for critical cases
- Audit trail for all recommendations
</constraints>

<forbidden_approaches>
- Guessing or imputing critical financial data
- Continuing with invalid inputs
- Recommendations without confidence scores
- Operating without monitoring
- No fail-safe defaults
</forbidden_approaches>
```

**Prompt 3** (Reliability Testing):
```xml
<task>
Create comprehensive reliability test suite
</task>

<test_requirements>
Edge Case Tests:
- Missing required client data
- Conflicting financial history
- Multiple accounts

Failure Mode Tests:
- Database unavailable
- Model service timeout
- Invalid model output
- Data quality issues
- High load conditions

Safety Tests:
- Verify human-in-the-loop for critical cases
- Confirm fail-safe defaults engage
- Test override mechanisms work
- Validate confidence thresholds
- Check alert system functions

Performance Tests:
- Response time under load
- Concurrent request handling
- Resource usage monitoring
- Degradation behavior
</test_requirements>
```