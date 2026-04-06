
import json
import logging
from app import generate_improvement_report, save_kpis_to_meeting
import config

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    meeting_id = "20260203_104028"
    from app import load_meetings
    logging.info(f"Loading meetings using app.load_meetings()")
    meetings = load_meetings()
    
    # Find the meeting
    meeting_index = -1
    meeting = None
    for i, m in enumerate(meetings):
        if m.get("meeting_id") == meeting_id:
            meeting = m
            meeting_index = i
            break
            
    if not meeting:
        logging.error(f"Meeting with ID {meeting_id} not found.")
        return

    logging.info(f"Found meeting: {meeting.get('title', 'Untitled')}")
    
    # Configure model
    logging.info("Configuring Gemini model...")
    try:
        model = config.configure()
    except Exception as e:
        logging.error(f"Failed to configure model: {e}")
        return

    # Generate report
    logging.info("Generating improvement report...")
    transcript = meeting.get("transcript", "")
    if not transcript:
         logging.error("No transcript found for this meeting.")
         return

    report_text, kpis, _ = generate_improvement_report([transcript], model)
    
    # Save Report to file
    report_filename = f"report_{meeting_id}.md"
    logging.info(f"Saving report to {report_filename}...")
    with open(report_filename, "w", encoding="utf8") as f:
        f.write(report_text)
        
    # Save KPIs to meeting
    if kpis:
        logging.info(f"Saving KPIs to meeting index {meeting_index}...")
        success = save_kpis_to_meeting(meeting_index, kpis)
        if success:
            logging.info(f"KPIs saved successfully: {json.dumps(kpis, indent=2)}")
        else:
            logging.error("Failed to save KPIs. save_kpis_to_meeting returned False.")
    else:
        logging.warning("No KPIs generated.")

    logging.info("Done.")

if __name__ == "__main__":
    main()
