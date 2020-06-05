import React, { Component } from "react";
import {
	Page,
	Navbar,
	Link,
	Toolbar,
	Block,
	Icon,
	BlockTitle,
	Button,
	Row,
	Col,
	Checkbox,
	List,
	ListItem,
} from "framework7-react";

export default class Home extends Component {
	constructor(props) {
		super(props);
		this.state = {
			question: "",
			answer: "",
			answers: [],
		};
	}

	componentWillMount() {
		this.newQuestion();
	}

	async newQuestion() {
		var content = await fetch("http://xnaclyy.pythonanywhere.com/random/");
		content = await content.json();

		this.setState({
			question: content.frage,
			answers: content.antworten,
			right: content.richtigeAntwort,
		});
	}

	select = (button) => {
		button = button.currentTarget;
		var answer = button.parentElement.getAttribute("answer");
		this.setState({ answer });
	};

	submit = () => {
		// console.log(this.state.answer);
		if (this.state.answer === this.state.right) {
			this.newQuestion();
			this.$f7.dialog.alert("", "Richtige Antwort");
		} else {
			this.$f7.dialog.alert("", "Falsche Antwort");
		}
	};

	render() {
		var answers = this.state.answers;
		var answer = this.state.answer;

		return (
			<Page name="home">
				<Navbar title="Quintic"></Navbar>
				<Block className="text-align-center">
					<BlockTitle>{this.state.question}</BlockTitle>
					<br></br>
					<Row>
						<Col>
							<span answer={answers[0]}>
								<Button
									onClick={this.select}
									color={answer === answers[0] ? "teal" : ""}
									large
									round
									raised
									fill
								>
									{answers[0]}
								</Button>
							</span>
						</Col>
						<Col>
							<span answer={answers[1]}>
								<Button
									onClick={this.select}
									color={answer === answers[1] ? "teal" : ""}
									large
									round
									raised
									fill
								>
									{answers[1]}
								</Button>
							</span>
						</Col>
					</Row>
					<br></br>
					<Row>
						<Col>
							<span answer={answers[2]}>
								<Button
									onClick={this.select}
									color={answer === answers[2] ? "teal" : ""}
									large
									round
									raised
									fill
								>
									{answers[2]}
								</Button>
							</span>
						</Col>
						<Col>
							<span answer={answers[3]}>
								<Button
									onClick={this.select}
									color={answer === answers[3] ? "teal" : ""}
									large
									round
									raised
									fill
								>
									{answers[3]}
								</Button>
							</span>
						</Col>
					</Row>
					<br></br>
					<Button
						large
						round
						raised
						fill
						color="green"
						onClick={this.submit}
					>
						Submit
					</Button>
				</Block>

				<Toolbar bottom>
					<Link
						external
						href="https://github.com/xNaCly/semikurs-code"
						target="blank"
					>
						Github
					</Link>
					<span onClick={window.switchDarkMode}>
						<Icon
							className="link"
							f7="lightbulb"
							tooltip="Toggle Darkmode"
						></Icon>
					</span>
				</Toolbar>
			</Page>
		);
	}
}
