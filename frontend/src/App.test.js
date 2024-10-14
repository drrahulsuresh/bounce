import { render, screen } from '@testing-library/react';
import App from './App';

test('renders the heading', () => {
  render(<App />);
  const headingElement = screen.getByText(/RAG Survey Insights/i);
  expect(headingElement).toBeInTheDocument();
});

test('renders the input box', () => {
  render(<App />);
  const inputElement = screen.getByPlaceholderText(/Enter your query/i);
  expect(inputElement).toBeInTheDocument();
});

test('renders the submit button', () => {
  render(<App />);
  const buttonElement = screen.getByText(/Submit Query/i);
  expect(buttonElement).toBeInTheDocument();
});
