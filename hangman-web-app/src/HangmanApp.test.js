import React from 'react';
import ReactDOM from 'react-dom';
import App from './HangmanApp';

it('renders without crashing', () => {
  const div = document.createElement('div');
  ReactDOM.render(<HangmanApp />, div);
  ReactDOM.unmountComponentAtNode(div);
});
