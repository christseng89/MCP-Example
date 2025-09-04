# BPMN Naming Conventions Best Practices

## Overview

Business Process Model and Notation (BPMN) naming conventions are crucial for creating clear, understandable, and maintainable process models. This guide outlines the best practices for naming BPMN elements.

## Core Principle: **Verb + Noun**

The primary naming convention for BPMN activities is **"Verb + Noun"**, which provides clarity and action-oriented descriptions.

## Element-Specific Naming Conventions

### 🔷 Activities/Tasks: Verb + Noun

**Pattern**: `[Action Verb] + [Object/Noun]`

**✅ Good Examples:**

- Process Invoice
- Approve Request
- Send Email
- Review Application
- Create Report
- Update Database
- Validate Data
- Generate Invoice

**❌ Poor Examples:**

- Invoice Processing
- Request Approval
- Email Sending
- Application Review

### 🔴 Events: Noun + Past Participle/State

**Start Events:**

- Customer Complaint
- Order Request
- Payment Due

**End Events:**

- Invoice Sent
- Process Completed
- Request Rejected
- Order Fulfilled

**Intermediate Events:**

- Payment Received
- Approval Timeout
- Document Updated
- Error Occurred

### 🔶 Gateways: Questions

**Pattern**: Clear yes/no questions or decision criteria

**✅ Good Examples:**

- Is Amount > $1000?
- Approved?
- Payment Method?
- Customer Type?
- Risk Level High?
- Valid Document?

### 📄 Data Objects: Nouns

**Pattern**: Clear, specific nouns

**✅ Good Examples:**

- Invoice
- Customer Data
- Approval Form
- Purchase Order
- Payment Receipt
- Contract Document

### 🏊 Pools and Lanes: Organizational Units

**Pattern**: Role or department names

**✅ Good Examples:**

- Customer Service
- Finance Department
- Sales Team
- IT Support
- External Vendor

## Key Principles

### 1. **Action-Oriented**

Activities should clearly indicate what action is being performed, making the process flow intuitive.

### 2. **Concise**

Keep names short but descriptive (2-4 words maximum). Avoid unnecessary articles and prepositions.

### 3. **Business Language**

Use terminology familiar to business stakeholders, not technical jargon.

### 4. **Consistent**

Apply the same naming pattern throughout your process models for better readability.

### 5. **Specific**

Be specific enough to avoid ambiguity while remaining concise.

### 6. **Standardized**

Follow organizational naming standards and conventions.

## Common Mistakes to Avoid

### ❌ Gerund Forms (-ing)

- **Wrong**: "Processing Invoice"
- **Right**: "Process Invoice"

### ❌ Passive Voice

- **Wrong**: "Invoice is Processed"
- **Right**: "Process Invoice"

### ❌ Vague Terms

- **Wrong**: "Handle Request"
- **Right**: "Approve Request" or "Review Request"

### ❌ Technical Jargon

- **Wrong**: "Execute SQL Query"
- **Right**: "Retrieve Customer Data"

## Examples by Industry

### Financial Services

- **Activities**: Process Loan, Verify Identity, Calculate Interest
- **Events**: Payment Received, Account Opened, Fraud Detected
- **Gateways**: Credit Score > 700?, Loan Approved?

### Healthcare

- **Activities**: Schedule Appointment, Review Medical History, Prescribe Medication
- **Events**: Patient Admitted, Test Results Available, Discharge Authorized
- **Gateways**: Emergency Case?, Insurance Covers?

### Manufacturing

- **Activities**: Assemble Product, Quality Check, Ship Order
- **Events**: Raw Materials Arrived, Production Complete, Defect Found
- **Gateways**: Quality Passed?, Stock Available?

## Tools and Implementation

### Modeling Tool Settings

- Configure naming templates in your BPMN tool
- Set up naming validation rules
- Use consistent fonts and formatting

### Team Guidelines

- Create naming convention checklists
- Conduct regular model reviews
- Maintain a glossary of approved terms

## Benefits of Good Naming Conventions

1. **Improved Communication** - Stakeholders understand processes quickly
2. **Better Maintenance** - Easier to update and modify processes
3. **Reduced Errors** - Clear naming prevents misunderstandings
4. **Enhanced Automation** - Facilitates process automation implementation
5. **Compliance Support** - Helps with audit and regulatory requirements

## Conclusion

Following the **"Verb + Noun"** convention for BPMN activities, combined with appropriate naming patterns for other elements, creates process models that are:

- Easy to read and understand
- Quick to navigate
- Simple to maintain
- Ready for automation

## Remember

Good naming conventions are an investment in the long-term success of your process modeling initiatives.

---

Last Updated: December 2024
