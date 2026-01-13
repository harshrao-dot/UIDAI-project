"""
Quick script to run the pipeline and generate insights.
"""
import sys
from main_pipeline import run_full_pipeline
from insights_generator import generate_insights
import json

if __name__ == '__main__':
    print("=" * 60)
    print("Aadhaar Identity Stress System - Pipeline Execution")
    print("=" * 60)
    
    try:
        results = run_full_pipeline()
        
        print("\n" + "=" * 60)
        print("Generating Insights...")
        print("=" * 60)
        
        insights = generate_insights(results)
        
        # Print insights
        print("\n[PRESENT] WHAT DATA SHOWS:")
        for finding in insights['present_findings']:
            print(f"\n  [{finding['category']}]")
            print(f"  {finding['finding']}")
            print(f"  Evidence: {finding['evidence']}")
        
        print("\n[SUGGESTIONS] ADMINISTRATIVE SUGGESTIONS:")
        for suggestion in insights['administrative_suggestions']:
            print(f"\n  [{suggestion['area']}]")
            print(f"  {suggestion['suggestion']}")
            print(f"  Rationale: {suggestion['rationale']}")
        
        print("\n[FUTURE RISKS] NEAR-FUTURE RISKS (2-5 YEARS):")
        for risk in insights['future_risks']:
            print(f"\n  [{risk['risk']}] ({risk['timeframe']})")
            print(f"  {risk['description']}")
            print(f"  Mitigation: {risk['mitigation']}")
        
        # Save insights to JSON
        from pathlib import Path
        output_dir = Path('processed_data')
        output_dir.mkdir(exist_ok=True)
        
        # Convert insights to JSON-serializable format
        insights_json = {
            'present_findings': insights['present_findings'],
            'administrative_suggestions': insights['administrative_suggestions'],
            'future_risks': insights['future_risks']
        }
        
        with open(output_dir / 'insights.json', 'w') as f:
            json.dump(insights_json, f, indent=2)
        
        print("\n" + "=" * 60)
        print("Pipeline completed successfully!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Review processed_data/ for output files")
        print("2. Run 'streamlit run app.py' to launch dashboard")
        print("3. Check processed_data/insights.json for structured insights")
        
    except Exception as e:
        print(f"\n[ERROR] Error during pipeline execution: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
