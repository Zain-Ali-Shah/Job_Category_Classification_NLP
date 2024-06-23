import React from "react";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import Container from "react-bootstrap/esm/Container";

const DescriptionForm = () => {
	const [description, setDescription] = React.useState("");
	const [predictedCategory, setPredictedCategory] = React.useState("");
	const handleChange = (e) => {
		setDescription(e.target.value);
	};
	const handleSubmit = async (e) => {
		e.preventDefault();
		try {
			const response = await fetch("http://localhost:5000/predict-category", {
				method: "POST",
				headers: {
					"Content-Type": "application/json",
				},
				body: JSON.stringify({ description }),
			});

			// Check if the response was successful
			if (response.ok) {
				const data = await response.json();
				// Display the predicted category on the frontend
				setPredictedCategory(data["prediction"]);
			} else {
				console.error("Error:", response.status);
			}
		} catch (error) {
			console.error("Error:", error);
		}
	};
	return (
		<Container style={{ minHeight: "70vh" }}>
			<Form onSubmit={handleSubmit} className="my-5">
				<Form.Group controlId="exampleForm.ControlTextarea1">
					<Form.Label>
						<h3>Job Description</h3>
					</Form.Label>
					<Form.Control
						type="text"
						name="description"
						as="textarea"
						rows={6}
						value={description}
						onChange={handleChange}
					/>
				</Form.Group>
				<Button className="my-3" variant="success" type="submit">
					Predict
				</Button>
			</Form>
			{predictedCategory && <h3>Predicted Category: {predictedCategory}</h3>}
		</Container>
	);
};

export default DescriptionForm;
