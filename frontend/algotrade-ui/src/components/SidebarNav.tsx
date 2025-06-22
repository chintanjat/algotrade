import React from 'react';
import { Layout, Menu } from 'antd';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  DashboardOutlined,
  SettingOutlined,
  BarChartOutlined,
  HistoryOutlined,
  LineChartOutlined,
} from '@ant-design/icons';

const { Sider } = Layout;

const SidebarNav: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  const menuItems = [
    {
      key: '/',
      icon: <DashboardOutlined />,
      label: 'Dashboard',
    },
    {
      key: '/strategies',
      icon: <SettingOutlined />,
      label: 'Strategies',
    },
    {
      key: '/positions',
      icon: <BarChartOutlined />,
      label: 'Positions',
    },
    {
      key: '/trades',
      icon: <HistoryOutlined />,
      label: 'Trade History',
    },
    {
      key: '/performance',
      icon: <LineChartOutlined />,
      label: 'Performance',
    },
  ];

  const handleMenuClick = ({ key }: { key: string }) => {
    navigate(key);
  };

  return (
    <Sider
      width={250}
      className="min-h-screen"
      theme="light"
    >
      <div className="p-6">
        <h1 className="text-2xl font-bold text-gradient">
          AlgoTrade
        </h1>
        <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
          Trading Dashboard
        </p>
      </div>
      
      <Menu
        mode="inline"
        selectedKeys={[location.pathname]}
        items={menuItems}
        onClick={handleMenuClick}
        className="border-0"
      />
      
      <div className="absolute bottom-6 left-6 right-6">
        <div className="text-xs text-gray-500 dark:text-gray-400 text-center">
          <p>Version 0.1.0</p>
          <p className="mt-1">Paper Trading Mode</p>
        </div>
      </div>
    </Sider>
  );
};

export default SidebarNav; 