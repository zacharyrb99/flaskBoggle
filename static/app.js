class BoggleGame {
  constructor(boardId, secs = 60) {
    this.secs = secs;
    this.showTime();

    this.score = 0;
    this.words = new Set();
    this.board = $("#" + boardId);
    this.time = setInterval(this.timeCounter.bind(this), 1000);

    $(".add-word", this.board).on("submit", this.handleWord.bind(this));
  }

  showScore() {
    $(".score", this.board).text(this.score);
  }

  showMessage(msg, cls) {
    $(".msg", this.board).text(msg).removeClass().addClass(`msg ${cls}`);
  }

  showWord(word) {
    $(".words", this.board).append($("<li>", { text: word }));
  }

  async handleWord(e) {
    e.preventDefault();
    const $word = $(".word", this.board);

    let word = $word.val();
    if (!word) return;

    if (this.words.has(word)) {
      this.showMessage(`Already found ${word}`);
      return;
    }

    const response = await axios.get("/check-word", { params: { word: word } });
    if (response.data.result === "not-word") {
      this.showMessage(`${word} is not a valid word for this game`, "error");
    } else if (response.data.result === "not-on-board") {
      this.showMessage(
        `${word} is a valid word, but not on this board.`,
        "error"
      );
    } else {
      this.score += word.length;
      this.showWord(word);
      this.showScore();
      this.words.add(word);
      this.showMessage(`Congrats, ${word} is valid!`, "success");
    }

    $word.val("").focus();
  }

  showTime() {
    $(".timer", this.board).text(this.secs);
  }

  async timeCounter() {
    this.secs -= 1;
    this.showTime();

    if (this.secs === 0) {
      clearInterval(this.time);
      await this.finalScore();
    }
  }

  async finalScore(){
    $(".add-word", this.board).hide();
    const response = await axios.post("/final-score", {score: this.score})
    if(response.data.brokeHighScore){
        this.showMessage(`New high score: ${this.score}`, "success")
    }else{
        this.showMessage(`Final Score: ${this.score}`, "success")
    }
  }
}
