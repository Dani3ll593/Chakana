class FeedbackManager:
    def __init__(self):
        self.feedback_data = {}

    def store_feedback(self, section, feedback):
        if section in self.feedback_data:
            self.feedback_data[section].append(feedback)
        else:
            self.feedback_data[section] = [feedback]

    def get_feedback(self, section):
        return self.feedback_data.get(section, [])