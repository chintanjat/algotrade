import React from 'react';
import { Typography } from 'antd';

const { Title } = Typography;

const Trades: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <Title level={2} className="!mb-2">
          Trade History
        </Title>
        <p className="text-gray-600 dark:text-gray-400">
          View your historical trading activity
        </p>
      </div>
      
      <div className="text-center py-12">
        <p className="text-gray-500 dark:text-gray-400">
          Trade history component will be implemented here
        </p>
      </div>
    </div>
  );
};

export default Trades; 