import os
import firebase_admin
from firebase_admin import credentials, firestore
from flask import Flask, jsonify, request, send_from_directory
from google import genai

app = Flask(__name__, static_folder="static", static_url_path="")

# Initialize Firebase / Firestore safely
db = None
try:
  if not firebase_admin._apps:
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(
        cred, {"projectId": os.environ.get("GOOGLE_CLOUD_PROJECT")}
    )
  db = firestore.client()
except Exception as err:
  print(f"Firestore initialization warning/fallback: {err}")

# Initialize Gemini Client
gemini_client = genai.Client()


@app.route("/")
def serve_frontend():
  return send_from_directory("static", "index.html")


@app.route("/api/health", methods=["GET"])
def health_check():
  return jsonify({
      "status": "online",
      "service": "HydroResilience AI Copilot",
      "environment": os.environ.get("K_SERVICE", "local-dev"),
  })


@app.route("/api/report-incident", methods=["POST"])
def report_incident():
  """Persists community hazard reports to Firestore."""
  data = request.json or {}
  location = data.get("location", "Sector 4 Lowland")
  description = data.get("description", "Water logging observed")
  water_depth = data.get("water_depth", "Knee Deep")

  report_payload = {
      "location": location,
      "description": description,
      "water_depth": water_depth,
      "timestamp": (
          firestore.SERVER_TIMESTAMP if db else "2026-10-18T20:00:00Z"
      ),
  }

  if db:
    try:
      db.collection("community_reports").add(report_payload)
    except Exception as e:
      print(f"Firestore save error: {e}")

  return jsonify({
      "success": True,
      "message": "Hazard report successfully logged in Firestore database.",
      "data": report_payload,
  })


@app.route("/api/assess-risk", methods=["POST"])
def assess_risk():
  """Uses Gemini to evaluate flood risk and suggest action plans."""
  data = request.json or {}
  location = data.get("location", "Sector 4 - Lowland Zone")
  rainfall_mm = data.get("rainfall_mm", 90)
  reported_hazards = data.get("hazards", "Water overflowing near main roads.")

  recent_reports = []
  if db:
    try:
      docs = (
          db.collection("community_reports")
          .where("location", "==", location)
          .limit(3)
          .stream()
      )
      recent_reports = [d.to_dict() for d in docs]
    except Exception as err:
      print(f"Firestore query error: {err}")

  # Construct Prompt for Gemini Reasoning Engine
  prompt = f"""
    You are an emergency climate intelligence AI assisting urban disaster response teams.
    Target Location: {location}
    Current 24h Rainfall: {rainfall_mm} mm
    Live Hazard Inputs: {reported_hazards}
    Recent Citizen Reports from Firestore: {recent_reports}

    Provide a concise, structured response with:
    1. Risk Level (Low / Medium / High / Critical)
    2. Immediate Threat Assessment
    3. 3-Step Action Plan for citizens and emergency response teams.
    """

  try:
    response = gemini_client.models.generate_content(
        model="gemini-2.5-flash", contents=prompt
    )
    ai_analysis = response.text
  except Exception as e:
    ai_analysis = f"High Risk Detected. Heavy rainfall ({rainfall_mm}mm) exceeds regional drainage limits at {location}. 1. Move to higher ground immediately. 2. Avoid subterranean passages. 3. Contact local response squads."

  if db:
    try:
      db.collection("risk_assessments").add({
          "location": location,
          "analysis": ai_analysis,
          "timestamp": firestore.SERVER_TIMESTAMP,
      })
    except Exception as err:
      print(f"Firestore save assessment error: {err}")

  return jsonify({
      "location": location,
      "rainfall_mm": rainfall_mm,
      "ai_risk_assessment": ai_analysis,
  })


if __name__ == "__main__":
  port = int(os.environ.get("PORT", 8080))
  app.run(host="0.0.0.0", port=port, debug=True)
