# Schema Design Explanation

This document explains the design decisions made for the database schema, focusing on the relationships, indexing, and constraints used in the models.

## Tables Overview

The schema includes the following entities:
1. **Permissions** - Defines permissions.
2. **Roles** - Represents user roles and their permissions within the system.
3. **Users** - Stores user details and their roles.
4. **Expenditure Requests** - Represents expenditure requests made by users.
5. **Approval Workflows** - Defines approval levels and officers responsible for different levels.
6. **Approvals** - Tracks the approval status of expenditure requests through the associated workflows.

---

## Schema Design Decisions

### 1. **Roles and Permissions**
- **Permissions** are permissions in the system's access control mechanism.
- **Roles** define different user roles in the system and their respective permissions (e.g., Project Owner, Manager, Finance Personnel, Oversight Committee).
- **Many-to-Many Relationship**: A role can have multiple permissions and a permission can be in multiple roles.
- **Indexes**:
  - `roles`: Indexed on `id` and `name` to optimize querying by these fields, since roles will often be looked up by their names.

### 2. **Users**
- **Users** store user details including their first name, last name, email, and associated roles.
- **Many-to-Many Relationship**: A user can have multiple roles, and a role can belong to multiple users. This is implemented using Django's `ManyToManyField`, allowing flexibility in assigning roles to users.
- **Unique Constraint**: `email` is unique for each user to ensure no duplicate entries.
- **Indexes**: The `id`, `email`, and `created_at` fields are indexed for efficient querying and enforcing uniqueness on `email`.

### 3. **Expenditure Requests**
- **Expenditure Requests** represent requests raised by users.
- **Many-to-One Relationship**: A user can raise many requests (`raised_by` foreign key).
- **Indexes**:
  - Optimized for querying by `id`, `created_at`, `title`, `raised_by`, `scope`, and `status`. These fields are frequently used in filtering and sorting requests.

### 4. **Approval Workflows**
- **Approval Workflows** define the levels of approval needed for a request and the officer responsible for each level.
- **Many-to-One Relationship**: Each workflow is associated with an approval process and approval officer (foreign key), and a user can be an officer in multiple workflows.
- **Unique Constraint**: combination of `level`, `approval` and `approval officer`  should be unique to ensure no duplication in levels and approval officers within a particular approval process.
- **Indexes**: Indexed on `id`, `created_at`, `level`, `approval`, `is_approved`, and `approval_officer` to enable quick lookup of workflows.

### 5. **Approvals**
- **Approvals** (`approvals`) track the approval status of each expenditure request as it moves through the approval workflow.
- **One-to-One Relationship**: Each `approval` links a specific `expenditure_request`.
- The approval status is recorded through the `is_completed` boolean field and `completed_on` timestamp.
- **Indexes**: The `id`, `created_at`, `request_id`, and `is_completed` fields are indexed to speed up the process of retrieving approvals based on request status and workflow level.

---

## Indexing Strategy

To optimize performance, especially for querying large datasets, we employed the following indexing strategies:
- **Primary Keys (`id`)**: Every table uses `id` as the primary key for uniquely identifying each record and since Django automatically creates index for primary keys, there's no need including `id` in indexes on the model class'
- **Frequent Query Fields**: Fields that are frequently queried or used in filtering operations, such as `name`, `email`, `created_at`, and foreign keys (`role_id`, `raised_by_id`, etc.), are indexed.

---

## Relationship Design

### Many-to-Many Relationship: Users and Roles
A user can have multiple roles (e.g., a project owner who is also a manager), and each role can be assigned to multiple users. The `ManyToManyField` in Django efficiently handles this relationship.

### Many-to-One Relationship: Approval Workflows-Approval and Requests-Users
The schema is designed to handle many-to-one relationships through foreign keys. For example, a user can raise multiple expenditure requests.
- On Request-User relationship, `raised_by` is set to null when its associated user is deleted, this is necessary as request still have other uses independent of its raiser.
- And approval workflow's approval officer is also set to null if its associated user is deleted for same reason as above.

### One-to-One Relationship: Approval and Requests
The schema is designed to handle one relationship between request and approval such that there can be no request with multiple approvals and vice-versa.
And approval is set to be deleted (CASCADE) when its request is deleted, there's no point keeping the approval.

### Approval Workflow and Requests
The approval workflow system is tightly integrated with `ExpenditureRequest` and `Approval`. Each request must pass through different workflow levels until it is completed. The workflow level is unique, ensuring a well-defined approval process.


---

## Conclusion

The schema is designed to be efficient, maintainable, and scalable. By using appropriate relationships and indexing frequently queried fields, we ensure that the system can handle a growing number of users, requests, and approvals while maintaining performance.
