import React, { useEffect, useState } from 'react';
import { Card, Statistic, Row, Col, Skeleton, notification } from 'antd';
import {
  DollarCircleOutlined,
  CheckCircleOutlined,
  RiseOutlined,
  SlidersOutlined
} from '@ant-design/icons';

interface CapitalSummary {
  totalPortfolioValue: number;
  availableCapital: number;
  allocatedCapital: number;
  totalPnl: number;
  dailyPnl: number;
}

const DashboardCards: React.FC = () => {
  const [summary, setSummary] = useState<CapitalSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSummary = async () => {
      try {
        setLoading(true);
        const response = await fetch('http://localhost:5000/api/capital/summary');
        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }
        const data: CapitalSummary = await response.json();
        setSummary(data);
      } catch (error) {
        console.error("Failed to fetch capital summary:", error);
        notification.error({
          message: 'Failed to Load Capital Summary',
          description: 'Could not connect to the backend. Please ensure it is running and try again.',
          placement: 'topRight',
        });
      } finally {
        setLoading(false);
      }
    };

    fetchSummary();
  }, []);

  const formatCurrency = (value: number) =>
    new Intl.NumberFormat('en-IN', {
      style: 'currency',
      currency: 'INR',
    }).format(value);

  const getPnlColor = (value: number) => {
    if (value > 0) return '#22c55e'; // green-500
    if (value < 0) return '#ef4444'; // red-500
    return '#6b7280'; // gray-500
  };

  if (loading) {
    return (
      <Row gutter={[16, 16]}>
        {[...Array(4)].map((_, i) => (
          <Col xs={24} sm={12} md={8} lg={6} key={i}>
            <Card>
              <Skeleton active paragraph={{ rows: 2 }} />
            </Card>
          </Col>
        ))}
      </Row>
    );
  }

  return (
    <Row gutter={[16, 16]}>
      <Col xs={24} sm={12} md={8} lg={6}>
        <Card>
          <Statistic
            title="Total Portfolio Value"
            value={summary?.totalPortfolioValue}
            precision={2}
            valueStyle={{ color: '#3b82f6' }}
            prefix={<DollarCircleOutlined />}
            formatter={(value) => formatCurrency(value as number)}
          />
        </Card>
      </Col>
      <Col xs={24} sm={12} md={8} lg={6}>
        <Card>
          <Statistic
            title="Available Capital"
            value={summary?.availableCapital}
            precision={2}
            valueStyle={{ color: '#10b981' }}
            prefix={<CheckCircleOutlined />}
            formatter={(value) => formatCurrency(value as number)}
          />
        </Card>
      </Col>
      <Col xs={24} sm={12} md={8} lg={6}>
        <Card>
          <Statistic
            title="Allocated Capital"
            value={summary?.allocatedCapital}
            precision={2}
            valueStyle={{ color: '#f59e0b' }}
            prefix={<SlidersOutlined />}
            formatter={(value) => formatCurrency(value as number)}
          />
        </Card>
      </Col>
      <Col xs={24} sm={12} md={8} lg={6}>
        <Card>
          <Statistic
            title="Total P&L"
            value={summary?.totalPnl}
            precision={2}
            valueStyle={{ color: getPnlColor(summary?.totalPnl ?? 0) }}
            prefix={<RiseOutlined />}
            formatter={(value) => formatCurrency(value as number)}
          />
           <div className="text-sm text-gray-500" style={{ color: getPnlColor(summary?.dailyPnl ?? 0)}}>
            Daily P&L: {formatCurrency(summary?.dailyPnl ?? 0)}
          </div>
        </Card>
      </Col>
    </Row>
  );
};

export default DashboardCards; 