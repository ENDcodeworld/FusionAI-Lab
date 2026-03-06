/**
 * FusionAI-Lab 前端应用入口
 * 核聚变 × AI 数据智能平台
 */

import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { ConfigProvider, Layout, Menu, theme } from 'antd';
import {
  DatabaseOutlined,
  LineChartOutlined,
  FileTextOutlined,
  HomeOutlined,
  GlobalOutlined,
  ThunderboltOutlined
} from '@ant-design/icons';
import type { MenuProps } from 'antd';
import FundingChart from './components/FundingChart';
import CompanyMap from './components/CompanyMap';

const { Header, Content, Footer } = Layout;

// 导航菜单
const menuItems: MenuProps['items'] = [
  {
    key: '/',
    icon: <HomeOutlined />,
    label: <Link to="/">首页</Link>,
  },
  {
    key: '/companies',
    icon: <DatabaseOutlined />,
    label: <Link to="/companies">公司数据库</Link>,
  },
  {
    key: '/funding',
    icon: <LineChartOutlined />,
    label: <Link to="/funding">融资追踪</Link>,
  },
  {
    key: '/reports',
    icon: <FileTextOutlined />,
    label: <Link to="/reports">行业报告</Link>,
  },
];

// 首页组件
const HomePage: React.FC = () => (
  <div style={{ padding: '24px' }}>
    <div style={{ textAlign: 'center', marginBottom: '48px' }}>
      <h1 style={{ fontSize: '48px', marginBottom: '16px' }}>
        <ThunderboltOutlined style={{ color: '#1890ff' }} /> FusionAI-Lab
      </h1>
      <p style={{ fontSize: '20px', color: '#666' }}>
        核聚变 × AI 数据智能平台
      </p>
      <p style={{ fontSize: '16px', color: '#999', marginTop: '24px' }}>
        追踪全球核聚变前沿，加速聚变能源商业化进程
      </p>
    </div>

    <div style={{ 
      display: 'grid', 
      gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', 
      gap: '24px',
      maxWidth: '1200px',
      margin: '0 auto'
    }}>
      <div style={{ 
        padding: '32px', 
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        borderRadius: '12px',
        color: 'white'
      }}>
        <DatabaseOutlined style={{ fontSize: '48px', marginBottom: '16px' }} />
        <h3>全球公司数据库</h3>
        <p>收录 40+ 核聚变公司，覆盖所有主流技术路线</p>
      </div>

      <div style={{ 
        padding: '32px', 
        background: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
        borderRadius: '12px',
        color: 'white'
      }}>
        <LineChartOutlined style={{ fontSize: '48px', marginBottom: '16px' }} />
        <h3>融资数据追踪</h3>
        <p>实时追踪 50+ 融资事件，总额超 50 亿美元</p>
      </div>

      <div style={{ 
        padding: '32px', 
        background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
        borderRadius: '12px',
        color: 'white'
      }}>
        <GlobalOutlined style={{ fontSize: '48px', marginBottom: '16px' }} />
        <h3>全球产业地图</h3>
        <p>可视化展示全球核聚变产业分布</p>
      </div>

      <div style={{ 
        padding: '32px', 
        background: 'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
        borderRadius: '12px',
        color: 'white'
      }}>
        <FileTextOutlined style={{ fontSize: '48px', marginBottom: '16px' }} />
        <h3>专业研究报告</h3>
        <p>深度行业分析和投资洞察</p>
      </div>
    </div>

    <div style={{ 
      marginTop: '48px', 
      padding: '32px', 
      background: '#f5f5f5', 
      borderRadius: '12px',
      textAlign: 'center'
    }}>
      <h2>核心功能</h2>
      <div style={{ 
        display: 'grid', 
        gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', 
        gap: '16px',
        marginTop: '24px'
      }}>
        <div>
          <h3>📊 公司数据库</h3>
          <p>详细信息、技术路线、融资历史</p>
        </div>
        <div>
          <h3>💰 融资追踪</h3>
          <p>实时数据、统计分析、趋势预测</p>
        </div>
        <div>
          <h3>📈 数据可视化</h3>
          <p>交互式图表、地理分布、时间线</p>
        </div>
        <div>
          <h3>📑 报告系统</h3>
          <p>年度报告、季度分析、公司研究</p>
        </div>
      </div>
    </div>
  </div>
);

// 报告页面组件
const ReportsPage: React.FC = () => (
  <div style={{ padding: '24px' }}>
    <h1>行业报告</h1>
    <p>专业的核聚变产业研究报告</p>
    
    <div style={{ marginTop: '24px', display: 'grid', gap: '16px' }}>
      <div style={{ padding: '24px', border: '1px solid #d9d9d9', borderRadius: '8px' }}>
        <h3>📊 2026 年全球核聚变产业年度概览</h3>
        <p>类型：年度报告 | 价格：免费</p>
        <p>包含全年融资统计、技术路线分析、主要投资事件和行业趋势预测。</p>
        <button style={{ 
          marginTop: '12px', 
          padding: '8px 24px', 
          background: '#1890ff', 
          color: 'white', 
          border: 'none', 
          borderRadius: '4px',
          cursor: 'pointer'
        }}>
          生成报告
        </button>
      </div>

      <div style={{ padding: '24px', border: '1px solid #d9d9d9', borderRadius: '8px' }}>
        <h3>📈 2026 年 Q1 核聚变产业季度报告</h3>
        <p>类型：季度报告 | 价格：¥199</p>
        <p>季度融资数据分析、新兴公司追踪、技术突破盘点。</p>
        <button style={{ 
          marginTop: '12px', 
          padding: '8px 24px', 
          background: '#1890ff', 
          color: 'white', 
          border: 'none', 
          borderRadius: '4px',
          cursor: 'pointer'
        }}>
          购买报告
        </button>
      </div>
    </div>
  </div>
);

const App: React.FC = () => {
  const {
    token: { colorBgContainer, borderRadiusLG },
  } = theme.useToken();

  return (
    <ConfigProvider
      theme={{
        token: {
          colorPrimary: '#1890ff',
        },
      }}
    >
      <Router>
        <Layout style={{ minHeight: '100vh' }}>
          <Header style={{ 
            display: 'flex', 
            alignItems: 'center', 
            background: colorBgContainer,
            padding: '0 24px',
            borderBottom: '1px solid #f0f0f0'
          }}>
            <div style={{ 
              fontSize: '20px', 
              fontWeight: 'bold',
              marginRight: '40px',
              color: '#1890ff'
            }}>
              <ThunderboltOutlined /> FusionAI-Lab
            </div>
            <Menu
              theme="light"
              mode="horizontal"
              selectedKeys={[]}
              items={menuItems}
              style={{ flex: 1, minWidth: 0 }}
            />
          </Header>
          
          <Content style={{ background: colorBgContainer }}>
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/companies" element={<CompanyMap />} />
              <Route path="/funding" element={<FundingChart />} />
              <Route path="/reports" element={<ReportsPage />} />
            </Routes>
          </Content>
          
          <Footer style={{ textAlign: 'center', background: colorBgContainer }}>
            <p>FusionAI-Lab ©2026 - 核聚变 × AI 数据智能平台</p>
            <p style={{ color: '#999', fontSize: '14px' }}>
              让聚变能源照亮未来 ⚛️
            </p>
          </Footer>
        </Layout>
      </Router>
    </ConfigProvider>
  );
};

export default App;
