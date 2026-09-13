# L4: Risks, Responsibilities, and the Limits of Trust - Exercises

This directory contains hands-on exercises for practicing risk assessment skills when working with AI-generated code, focusing on security, ethical, and reliability considerations.

## Learning Objectives

By completing these exercises, you will be able to:
- Identify security vulnerabilities in AI-generated code
- Assess ethical implications of algorithmic decision-making
- Evaluate reliability risks in production systems
- Apply systematic risk assessment frameworks
- Make professional decisions about AI code acceptance
- Understand your responsibility as the reviewing engineer

## Risk Assessment Framework

Use this systematic approach for all AI code risk assessments:

### 1. Security Risk Assessment
- [ ] Input validation and sanitization
- [ ] Authentication and authorization implementation
- [ ] Data protection and encryption
- [ ] SQL injection and other injection vulnerabilities
- [ ] Error handling that doesn't leak sensitive information

### 2. Ethical Risk Assessment
- [ ] Fairness and non-discrimination in algorithmic decisions
- [ ] Privacy and data consent considerations
- [ ] Transparency and explainability of automated decisions
- [ ] Potential for harm or misuse
- [ ] Impact on affected communities and stakeholders

### 3. Reliability Risk Assessment
- [ ] Resource management (memory, connections, file handles)
- [ ] Error handling for external dependencies
- [ ] Performance under load and edge conditions
- [ ] Graceful degradation and recovery mechanisms
- [ ] Monitoring and observability considerations

### 4. Professional Responsibility
- [ ] Risk level appropriate for verification depth
- [ ] Documentation of assessment process
- [ ] Stakeholder consultation when needed
- [ ] Escalation for high-risk components

## Exercise Structure

Each exercise follows this structure:

```
concept#-exercise-name/
├── starter/
│   ├── code_file.py          # AI-generated code to assess
│   ├── test_code_file.py     # Tests to run
│   └── requirements.txt      # Dependencies
└── solution/
    ├── code_file.py          # Improved version
    ├── risk_assessment.md    # Detailed risk analysis
    └── test_code_file.py     # Enhanced tests
```

## Exercises Overview

### Concept 1: Security Vulnerability Assessment
**Focus:** Identifying security vulnerabilities in AI-generated authentication and data handling code
**Skills:** Security review, vulnerability identification, secure coding patterns
**Risk Level:** High (handles sensitive user data)

### Concept 2: Ethical Impact Analysis
**Focus:** Assessing bias and fairness in AI-generated recommendation and scoring algorithms
**Skills:** Ethical reasoning, bias detection, fairness evaluation
**Risk Level:** Medium-High (affects user opportunities and experiences)

### Concept 3: Reliability Risk Assessment
**Focus:** Evaluating reliability issues in AI-generated batch processing and API integration code
**Skills:** Reliability analysis, error handling design, performance considerations
**Risk Level:** Medium (affects system availability and user experience)

### Concept 4: Complete Risk Assessment
**Focus:** Comprehensive evaluation of AI-generated healthcare data processing system
**Skills:** Integrated risk assessment, professional judgment, escalation decisions
**Risk Level:** Critical (healthcare domain with strict compliance requirements)

## How to Complete Each Exercise

1. **Review the starter code** for security, ethical, and reliability issues
2. **Apply the risk assessment framework** systematically
3. **Classify the risk level** (Low, Medium, High, Critical)
4. **Document specific vulnerabilities** and concerns found
5. **Determine verification requirements** based on risk level
6. **Make an acceptance decision**: Accept, Modify, Reject, or Escalate
7. **Run the provided tests** to understand functionality
8. **Compare with solution** to validate your assessment
9. **Study the improved implementation** and risk mitigation strategies

## Assessment Criteria

Your risk assessments will be evaluated on:

- **Security Awareness**: Can you identify security vulnerabilities and attack vectors?
- **Ethical Reasoning**: Do you consider fairness, bias, and social impact?
- **Reliability Analysis**: Can you spot resource management and error handling issues?
- **Risk Classification**: Do you accurately assess the risk level?
- **Professional Judgment**: Are your acceptance decisions appropriate and defensible?
- **Documentation Quality**: Is your assessment thorough and well-reasoned?

## Exercise Completion

Complete all 4 concepts to build comprehensive risk assessment skills:

1. **Security Assessment**: Learn to identify and mitigate security vulnerabilities
2. **Ethical Analysis**: Develop skills for evaluating algorithmic fairness and bias
3. **Reliability Evaluation**: Master techniques for assessing system reliability
4. **Integrated Assessment**: Practice making complex professional decisions

## Testing and Validation

Each exercise includes tests to help you understand:
- **Functional behavior** of the AI-generated code
- **Security vulnerabilities** through penetration testing
- **Performance characteristics** under load
- **Edge cases** and error conditions

Run tests with:
```bash
cd concept#-exercise-name/starter
pip install -r requirements.txt
pytest test_*.py -v
```

Remember: The goal isn't to distrust AI-generated code, but to collaborate with AI responsibly while maintaining professional engineering standards.