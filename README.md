# HydroResilience AI — Urban Flood Resilience Copilot 🌊

> Built for the **Google Cloud AI Builder Cup 2026** | **Challenge 6: Sustainability & Social Impact**

HydroResilience AI is an AI-powered climate adaptation and disaster response solution designed to strengthen community resilience during urban flooding and extreme weather events. The platform synthesizes real-time community reports, environmental metrics, and natural language reasoning to provide actionable safety guidance for citizens and emergency teams.

---

## 🛠️ Technology Stack & Architecture

- **Gemini (Vertex AI / Google AI Studio):** Powers the conversational intelligence and reasoning engine, synthesizing multi-modal flood inputs and citizen reports into localized action plans.
- **Google Cloud Run:** Serverless host for our containerized Python microservice API backend and web assets.
- **Firebase / Firestore:** Handles real-time NoSQL document storage and state management for active hazard alerts and community reports.
- **Firebase Hosting & Auth:** Web client delivery and user access management.

---

## 🚀 Local Setup & Installation

### Prerequisites
- Python 3.10+
- Google Cloud SDK (`gcloud` CLI)
- Active GCP Project with Vertex AI & Cloud Run APIs enabled

### Running Locally

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/Keerthi786/AI_Builder_Cup_Sustainability-Social-Impact.git](https://github.com/Keerthi786/AI_Builder_Cup_Sustainability-Social-Impact.git)
   cd AI_Builder_Cup_Sustainability-Social-Impact
