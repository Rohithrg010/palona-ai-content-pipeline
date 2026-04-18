from generate_content import generate_content
from crm import run_crm_workflow
from analysis import run_analysis


def main():
    print("🚀 AI Marketing Pipeline")
    topic = input("Enter a topic: ")

    print("\nStep 1: Generating content...")
    generate_content(topic)

    print("\nStep 2: Running CRM workflow...")
    run_crm_workflow()

    print("\nStep 3: Running performance analysis...")
    run_analysis()

    print("\n✅ Pipeline completed successfully!")


if __name__ == "__main__":
    main()
