import pandas as pd
import matplotlib.pyplot as plt
def visualize_mood_journal(csv_file="C:\\Documents\\projects\\NewChatbot\\data\\mood_journal.csv", output_file="mood_trend.png"):
        # Read the mood journal CSV
        df = pd.read_csv(csv_file, names=["timestamp", "mood"])

        # Map mood to numbers
        mood_mapping = {"sad": 0, "neutral": 1, "happy": 2}
        df['mood_value'] = df['mood'].map(mood_mapping)

        # Convert timestamps to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])

        # Create the plot
        plt.figure(figsize=(10, 4))
        plt.plot(df['timestamp'], df['mood_value'], marker='o', linestyle='-', color='blue')
        plt.yticks([0, 1, 2], ['Sad', 'Neutral', 'Happy'])
        plt.xlabel('Time')
        plt.ylabel('Mood')
        plt.title('Your Mood Over Time 🧠💬')
        plt.grid(True)
        plt.tight_layout()

        # Overwrite the same file every time
        plt.savefig(output_file)
        plt.close()
        print(f"Mood trend graph updated: {output_file}")