import "bootstrap/dist/css/bootstrap.min.css";
import "./App.css";
import Header from "./components/Header";
import DescriptionForm from "./components/DescriptionForm";
import Footer from "./components/Footer";

function App() {
	return (
		<>
			<Header />
			<DescriptionForm />
			<Footer />
		</>
	);
}

export default App;
