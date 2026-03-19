# Product Breakdown Structure (PBS) - Participium

This document provides a hierarchical decomposition of the deliverables for the Participium project. Each entry represents an observable output, as required by the project management standards.

| ID | Deliverable | Type | Notes |
|:---|:------------|:-----|:------|
| **1.0** | **Software System** | **Product** | The integrated Participium web platform. |
| 1.1 | Frontend Web Application | Component | Responsive UI for all user roles. |
| 1.1.1 | Public Consultation Portal | Feature | Map view (OSM), table view, and public statistics. |
| 1.1.2 | Citizen Dashboard | Feature | Report submission workflow, personal history, and "follow" list. |
| 1.1.3 | Admin/Operator Interface | Feature | Report management (approval/routing), direct messaging, and analytics. |
| 1.2 | Backend API Services | Component | Server-side logic and business rules. |
| 1.2.1 | Auth & User Management Service | Service | Identity management, registration, and email verification. |
| 1.2.2 | Geo-Report Engine | Service | Lifecycle management of reports with GIS data handling. |
| 1.2.3 | Communication & Notification Hub | Service | In-app notifications, email dispatch, and messaging. |
| 1.3 | Persistence Layer | Component | Data and asset storage solutions. |
| 1.3.1 | Geo-spatial Database | Database | Relational storage with GIS extensions (e.g., PostGIS). |
| 1.3.2 | Media Object Storage | Storage | Repository for report photos (up to 3 per report). |
| **2.0** | **Project Documentation** | **Product** | Technical and management artifacts. |
| 2.1 | Functional Requirements Spec | Document | Detailed user stories, status transitions, and data models. |
| 2.2 | Architectural Design Document | Document | System diagrams, API specifications, and infrastructure schema. |
| 2.3 | Project Management Artifacts | Document | Finalized PBS, WBS, Gantt Schedule, and Risk Register. |
| 2.4 | Deployment & Ops Manual | Document | Instructions for system setup, maintenance, and backup. |
| 2.5 | User & Operator Guides | Document | Training materials for citizens and municipal staff. |
| **3.0** | **Infrastructure & DevOps** | **Product** | Technical environment for delivery. |
| 3.1 | Cloud Hosting Environments | Environment | Configured Staging and Production instances. |
| 3.2 | CI/CD Automation Pipeline | Tooling | Automated build, test, and deployment workflows. |

---

## Rationale & Assumptions
- **Scope Interpretation:** The PBS focuses on the core functional requirements (reporting, mapping, messaging) and the administrative needs (moderation, analytics).
- **Deliverable Type:** Every item is a tangible "thing" (a service, a document, a configured environment) that can be signed off upon completion.
- **Assumptions:** We assume a modern web stack (React/Node.js or similar) where the frontend and backend are distinct deliverables. The use of OpenStreetMap is reflected in the Geo-Report Engine (1.2.2).
