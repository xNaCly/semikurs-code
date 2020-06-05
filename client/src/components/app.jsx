import React from "react";
import { App, View } from "framework7-react";
import routes from "../js/routes";

export default class extends React.Component {
	constructor() {
		super();

		this.state = {
			// Framework7 Parameters
			f7params: {
				name: "Quintic",
				theme: "ios",
				routes: routes,
			},
			darkmode: true,
		};
		window.switchDarkMode = this.switchDarkMode.bind(this);
	}


	switchDarkMode() {
		this.setState({ darkmode: !this.state.darkmode });
	}

	render() {
		return (
			<App params={this.state.f7params} themeDark={this.state.darkmode}>
				<View
					main
					className="safe-areas"
					url="/"
					pushState
					pushStateRoot=""
					pushStateSeparator={location.origin}
				/>
			</App>
		);
	}
}
