import React from 'react';
import { Typography } from 'antd';

const { Title } = Typography;

const Performance: React.FC = () => {
  return (
    <div className="space-y-6">
      <div>
        <Title level={2} className="!mb-2">
          Performance Analytics
        </Title>
        <p className="text-gray-600 dark:text-gray-400">
          Analyze your trading performance and metrics
        </p>
      </div>
      
      <div className="text-center py-12">
        <p className="text-gray-500 dark:text-gray-400">
          Performance analytics component will be implemented here
        </p>
      </div>
    </div>
  );
};

export default Performance; 