import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Layout, theme } from 'antd';
import SidebarNav from './components/SidebarNav';
import Topbar from './components/Topbar';
import Dashboard from './pages/Dashboard';
import Strategies from './pages/Strategies';
import Positions from './pages/Positions';
import Trades from './pages/Trades';
import Performance from './pages/Performance';
import './index.css';

const { Content, Sider } = Layout;

const App: React.FC = () => {
  const {
    token: { colorBgContainer },
  } = theme.useToken();

  return (
    <Router>
      <Layout style={{ minHeight: '100vh' }}>
        <Sider width={250} theme="dark">
          <SidebarNav />
        </Sider>
        <Layout>
          <Topbar />
          <Content style={{ padding: '24px', background: colorBgContainer }}>
            <div className="max-w-screen-2xl mx-auto">
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/strategies" element={<Strategies />} />
                <Route path="/positions" element={<Positions />} />
                <Route path="/trades" element={<Trades />} />
                <Route path="/performance" element={<Performance />} />
              </Routes>
            </div>
          </Content>
        </Layout>
      </Layout>
    </Router>
  );
};

export default App; 