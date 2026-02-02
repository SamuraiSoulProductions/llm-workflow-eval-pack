# Security Policy

## Synthetic Data Only

This repository is a **demonstration project** for agent reliability and security engineering practices. All test data is fully synthetic and does not contain:

- Real customer information
- Actual business policies or procedures
- Production credentials or API keys
- Proprietary data from any organization
- Real phone numbers, addresses, or contact information

## Secure Contribution Guidelines

When contributing to this project:

### ✅ DO:
- Use synthetic, fictional data for all examples
- Generate realistic-looking but fake phone numbers (e.g., 555-0100)
- Create generic business scenarios without identifying real companies
- Use placeholder credentials like `synthetic_user_123`
- Document security patterns and anti-patterns with synthetic examples

### ❌ DO NOT:
- Include real customer data or PII
- Commit actual API keys, passwords, or secrets (even expired ones)
- Reference proprietary business logic from real companies
- Include production logs or error messages
- Add real phone numbers, even if publicly available

## Reporting Vulnerabilities

This is a demonstration/educational project, not a production system. However, if you identify:

1. **Code patterns that demonstrate poor security practices**: Open an issue describing the concern
2. **Accidentally committed sensitive data**: Email the repository owner immediately before opening a public issue
3. **Dependency vulnerabilities**: Open a pull request updating the affected dependencies (though this project uses standard library only)

### Responsible Disclosure

If you discover that real data has been accidentally included:

1. **Do not** open a public issue
2. Email the repository maintainer with details
3. Allow 48 hours for response and remediation
4. After remediation, a public acknowledgment will be made (if you wish to be credited)

## Security Engineering Principles Demonstrated

This repository showcases defensive engineering practices:

- **Input validation**: Prompt injection detection and refusal
- **Verified sources**: No hallucinated contact information
- **Deterministic fallbacks**: Safe escalation on tool failures
- **Regression protection**: Eval gating for behavior changes
- **Fail-safe defaults**: Unknown inputs → clarify, not invent

These patterns are demonstrated with synthetic data to protect real user privacy while teaching production-grade reliability practices.

## Out of Scope

The following are not security concerns for this repository:

- Performance optimizations (this is a demo, not production code)
- Advanced attack vectors beyond prompt injection basics
- Infrastructure security (no deployed services)
- Rate limiting or DDoS protection (no external API)

## License and Liability

This code is provided for educational purposes. Users are responsible for adapting these patterns appropriately to their production environments with proper security reviews.
