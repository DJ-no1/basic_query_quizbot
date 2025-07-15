// QuizBot Frontend Application
class QuizBot {
  constructor() {
    this.apiUrl = "http://localhost:8000";
    this.currentQuiz = null;
    this.currentQuestionIndex = 0;
    this.sessionId = null;
    this.userAnswers = [];
    this.score = 0;

    this.initializeApp();
  }

  initializeApp() {
    this.loadSuggestedTopics();
    this.setupEventListeners();
  }

  setupEventListeners() {
    // Topic form submission
    document.getElementById("topicForm").addEventListener("submit", (e) => {
      e.preventDefault();
      this.generateQuiz();
    });

    // Suggested topic clicks
    document
      .getElementById("suggestedTopics")
      .addEventListener("click", (e) => {
        if (e.target.classList.contains("suggested-topic")) {
          document.getElementById("topic").value = e.target.textContent;
        }
      });

    // Navigation buttons
    document.getElementById("prevBtn").addEventListener("click", () => {
      this.previousQuestion();
    });

    document.getElementById("nextBtn").addEventListener("click", () => {
      this.nextQuestion();
    });

    document.getElementById("finishBtn").addEventListener("click", () => {
      this.finishQuiz();
    });

    // Results screen buttons
    document.getElementById("newQuizBtn").addEventListener("click", () => {
      this.startNewQuiz();
    });

    document.getElementById("retryBtn").addEventListener("click", () => {
      this.retryQuiz();
    });

    document.getElementById("resetBtn").addEventListener("click", () => {
      this.resetCurrentQuiz();
    });
  }

  async loadSuggestedTopics() {
    try {
      const response = await fetch(`${this.apiUrl}/quiz/topics`);
      const data = await response.json();

      const container = document.getElementById("suggestedTopics");
      container.innerHTML = "";

      data.suggested_topics.slice(0, 9).forEach((topic) => {
        const button = document.createElement("button");
        button.className =
          "suggested-topic bg-blue-100 hover:bg-blue-200 text-blue-800 text-sm font-medium py-2 px-4 rounded-full transition-colors";
        button.textContent = topic;
        container.appendChild(button);
      });
    } catch (error) {
      console.error("Error loading suggested topics:", error);
    }
  }

  async generateQuiz() {
    const topic = document.getElementById("topic").value.trim();
    const numQuestions = parseInt(
      document.getElementById("numQuestions").value
    );
    const difficulty = document.getElementById("difficulty").value;

    if (!topic) {
      alert("Please enter a topic for the quiz");
      return;
    }

    this.showScreen("loadingScreen");

    try {
      const response = await fetch(`${this.apiUrl}/quiz/generate`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          topic: topic,
          num_questions: numQuestions,
          difficulty: difficulty,
        }),
      });

      const data = await response.json();

      if (data.success) {
        this.currentQuiz = data.quiz;
        this.sessionId = data.session_id;
        this.currentQuestionIndex = 0;
        this.userAnswers = [];
        this.score = 0;
        this.startQuiz();
      } else {
        throw new Error(data.error || "Failed to generate quiz");
      }
    } catch (error) {
      console.error("Error generating quiz:", error);
      alert("Failed to generate quiz. Please try again.");
      this.showScreen("topicScreen");
    }
  }

  startQuiz() {
    this.showScreen("quizScreen");
    document.getElementById("quizTopic").textContent = this.currentQuiz.topic;
    document.getElementById("scoreDisplay").classList.remove("hidden");
    document.getElementById("resetBtn").classList.remove("hidden");
    this.displayQuestion();
  }

  displayQuestion() {
    const question = this.currentQuiz.questions[this.currentQuestionIndex];
    const totalQuestions = this.currentQuiz.total_questions;

    // Update question text and progress
    document.getElementById("questionText").textContent = question.question;
    document.getElementById("questionProgress").textContent = `Question ${
      this.currentQuestionIndex + 1
    } of ${totalQuestions}`;

    // Update progress bar
    const progressPercentage =
      ((this.currentQuestionIndex + 1) / totalQuestions) * 100;
    document.getElementById(
      "progressBar"
    ).style.width = `${progressPercentage}%`;

    // Create options
    const optionsContainer = document.getElementById("optionsContainer");
    optionsContainer.innerHTML = "";

    question.options.forEach((option, index) => {
      const button = document.createElement("button");
      button.className =
        "option-button w-full text-left p-4 border-2 border-gray-200 rounded-lg hover:border-blue-400 hover:bg-blue-50 transition-all duration-200";
      button.innerHTML = `
                <div class="flex items-center space-x-3">
                    <span class="flex-shrink-0 w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center font-semibold text-gray-600">
                        ${String.fromCharCode(65 + index)}
                    </span>
                    <span class="flex-1">${option}</span>
                </div>
            `;

      button.addEventListener("click", () => {
        this.selectOption(index);
      });

      optionsContainer.appendChild(button);
    });

    // Hide feedback
    document.getElementById("feedback").classList.add("hidden");

    // Update navigation buttons
    this.updateNavigationButtons();
  }

  async selectOption(optionIndex) {
    // Disable all option buttons
    const optionButtons = document.querySelectorAll(".option-button");
    optionButtons.forEach((btn) => (btn.disabled = true));

    try {
      const response = await fetch(
        `${this.apiUrl}/quiz/answer?session_id=${this.sessionId}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            question_index: this.currentQuestionIndex,
            selected_option: optionIndex,
          }),
        }
      );

      const result = await response.json();

      // Store the answer
      this.userAnswers[this.currentQuestionIndex] = {
        selected: optionIndex,
        correct: result.correct,
        score_change: result.score_change,
      };

      // Update score
      this.score += result.score_change;
      this.updateScoreDisplay();

      // Show feedback
      this.showFeedback(result, optionIndex);

      // Update option buttons to show correct/incorrect
      optionButtons.forEach((btn, index) => {
        if (index === result.correct_answer) {
          btn.classList.add("correct");
        } else if (index === optionIndex && !result.correct) {
          btn.classList.add("incorrect");
        }
      });

      // Show next/finish button
      if (this.currentQuestionIndex < this.currentQuiz.total_questions - 1) {
        document.getElementById("nextBtn").classList.remove("hidden");
      } else {
        document.getElementById("finishBtn").classList.remove("hidden");
      }
    } catch (error) {
      console.error("Error submitting answer:", error);
      alert("Failed to submit answer. Please try again.");
      // Re-enable buttons
      optionButtons.forEach((btn) => (btn.disabled = false));
    }
  }

  showFeedback(result, selectedOption) {
    const feedback = document.getElementById("feedback");
    const feedbackIcon = document.getElementById("feedbackIcon");
    const feedbackText = document.getElementById("feedbackText");
    const explanationText = document.getElementById("explanationText");

    if (result.correct) {
      feedback.className =
        "bg-green-50 border border-green-200 p-4 rounded-lg mb-6";
      feedbackIcon.className =
        "fas fa-check-circle text-green-600 text-2xl mt-1";
      feedbackText.textContent = `Correct! (+${result.score_change} points)`;
      feedbackText.className = "font-semibold mb-2 text-green-800";
    } else {
      feedback.className =
        "bg-red-50 border border-red-200 p-4 rounded-lg mb-6";
      feedbackIcon.className = "fas fa-times-circle text-red-600 text-2xl mt-1";
      feedbackText.textContent = `Incorrect (${result.score_change} points)`;
      feedbackText.className = "font-semibold mb-2 text-red-800";
    }

    explanationText.textContent = result.explanation;
    explanationText.className = "text-sm text-gray-700";

    feedback.classList.remove("hidden");
  }

  updateScoreDisplay() {
    document.getElementById("currentScore").textContent = this.score;
    document.getElementById("quizScore").textContent = `Score: ${this.score}`;
  }

  updateNavigationButtons() {
    const prevBtn = document.getElementById("prevBtn");
    const nextBtn = document.getElementById("nextBtn");
    const finishBtn = document.getElementById("finishBtn");

    // Previous button
    prevBtn.disabled = this.currentQuestionIndex === 0;

    // Hide next/finish buttons initially
    nextBtn.classList.add("hidden");
    finishBtn.classList.add("hidden");
  }

  previousQuestion() {
    if (this.currentQuestionIndex > 0) {
      this.currentQuestionIndex--;
      this.displayQuestion();
    }
  }

  nextQuestion() {
    if (this.currentQuestionIndex < this.currentQuiz.total_questions - 1) {
      this.currentQuestionIndex++;
      this.displayQuestion();
    }
  }

  async finishQuiz() {
    try {
      const response = await fetch(
        `${this.apiUrl}/quiz/score/${this.sessionId}`
      );
      const scoreData = await response.json();

      this.showResults(scoreData);
    } catch (error) {
      console.error("Error getting final score:", error);
      alert("Failed to get final score. Please try again.");
    }
  }

  showResults(scoreData) {
    this.showScreen("resultsScreen");

    // Update score displays
    document.getElementById("finalScore").textContent = scoreData.current_score;
    document.getElementById("correctAnswers").textContent =
      scoreData.correct_answers;
    document.getElementById("incorrectAnswers").textContent =
      scoreData.incorrect_answers;

    // Update accuracy
    const accuracy = Math.round(scoreData.percentage);
    document.getElementById("accuracyText").textContent = `${accuracy}%`;

    // Animate accuracy bar
    setTimeout(() => {
      document.getElementById("accuracyBar").style.width = `${accuracy}%`;
    }, 500);

    // Set result icon based on performance
    const resultIcon = document.getElementById("resultIcon");
    if (accuracy >= 80) {
      resultIcon.className = "fas fa-trophy text-yellow-500 text-6xl mb-4";
    } else if (accuracy >= 60) {
      resultIcon.className = "fas fa-thumbs-up text-green-500 text-6xl mb-4";
    } else {
      resultIcon.className =
        "fas fa-graduation-cap text-blue-500 text-6xl mb-4";
    }
  }

  startNewQuiz() {
    this.currentQuiz = null;
    this.sessionId = null;
    this.currentQuestionIndex = 0;
    this.userAnswers = [];
    this.score = 0;

    document.getElementById("scoreDisplay").classList.add("hidden");
    document.getElementById("resetBtn").classList.add("hidden");
    document.getElementById("topic").value = "";

    this.showScreen("topicScreen");
  }

  async retryQuiz() {
    if (this.sessionId) {
      try {
        await fetch(`${this.apiUrl}/quiz/reset/${this.sessionId}`, {
          method: "POST",
        });

        this.currentQuestionIndex = 0;
        this.userAnswers = [];
        this.score = 0;
        this.updateScoreDisplay();
        this.startQuiz();
      } catch (error) {
        console.error("Error resetting quiz:", error);
        alert("Failed to reset quiz. Please try again.");
      }
    }
  }

  async resetCurrentQuiz() {
    if (
      this.sessionId &&
      confirm("Are you sure you want to reset your current progress?")
    ) {
      await this.retryQuiz();
    }
  }

  showScreen(screenId) {
    // Hide all screens
    const screens = [
      "topicScreen",
      "loadingScreen",
      "quizScreen",
      "resultsScreen",
    ];
    screens.forEach((screen) => {
      document.getElementById(screen).classList.add("hidden");
    });

    // Show the requested screen
    document.getElementById(screenId).classList.remove("hidden");
  }
}

// Initialize the app when DOM is loaded
document.addEventListener("DOMContentLoaded", () => {
  new QuizBot();
});

// Service Worker registration for PWA capabilities (optional)
if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker
      .register("/sw.js")
      .then((registration) => {
        console.log("SW registered: ", registration);
      })
      .catch((registrationError) => {
        console.log("SW registration failed: ", registrationError);
      });
  });
}
