import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import './index.scss';
import Layout from './layouts/Layout';

ReactDOM.createRoot(document.getElementById('root') as HTMLElement).render(
  <React.StrictMode>
    <Layout>
      <App />
    </Layout>
  </React.StrictMode>
);
