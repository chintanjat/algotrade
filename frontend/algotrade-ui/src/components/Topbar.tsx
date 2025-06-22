import React from 'react';
import { Layout, Input, Avatar, Badge, Space } from 'antd';
import { BellOutlined, SettingOutlined, UserOutlined } from '@ant-design/icons';

const { Header } = Layout;

const Topbar: React.FC = () => {
  return (
    <Header
      className="flex items-center justify-between px-6 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 sticky top-0 z-10"
      style={{ padding: '0 24px' }}
    >
      <div>
        <Input.Search
          placeholder="Search strategies, symbols..."
          style={{ width: 300 }}
        />
      </div>

      <div className="flex items-center">
        <Space size="middle">
          <Badge count={5}>
            <BellOutlined style={{ fontSize: '18px' }} />
          </Badge>
          <SettingOutlined style={{ fontSize: '18px' }} />
          <Avatar icon={<UserOutlined />} />
        </Space>
      </div>
    </Header>
  );
};

export default Topbar; 