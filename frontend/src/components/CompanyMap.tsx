/**
 * 全球核聚变公司地理分布图
 */

import React, { useEffect, useState } from 'react';
import ReactECharts from 'echarts-for-react';
import { Card, Spin, Table, Tag } from 'antd';
import axios from 'axios';

interface Company {
  id: number;
  name: string;
  country: string;
  founded_year: number;
  technology_type: string;
  website?: string;
  description?: string;
}

const API_BASE = '/api/v1';

const CompanyMap: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [companies, setCompanies] = useState<Company[]>([]);

  useEffect(() => {
    fetchCompanies();
  }, []);

  const fetchCompanies = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${API_BASE}/companies?limit=100`);
      setCompanies(response.data);
    } catch (error) {
      console.error('Failed to fetch companies:', error);
    } finally {
      setLoading(false);
    }
  };

  // 按国家统计公司数量
  const countryStats = companies.reduce((acc, company) => {
    acc[company.country] = (acc[company.country] || 0) + 1;
    return acc;
  }, {} as Record<string, number>);

  // 地图配置
  const mapOption = {
    title: {
      text: '全球核聚变公司分布',
      left: 'center',
      top: 20
    },
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => {
        return `${params.name}<br/>公司数量：${params.value}`;
      }
    },
    visualMap: {
      min: 0,
      max: 10,
      left: 'left',
      top: 'bottom',
      text: ['高', '低'],
      calculable: true,
      inRange: {
        color: ['#e0f3f8', '#abd9e9', '#74add1', '#4575b4', '#313695']
      }
    },
    geo: {
      map: 'world',
      roam: true,
      label: {
        show: false
      },
      itemStyle: {
        areaColor: '#f3f3f3',
        borderColor: '#999',
        borderWidth: 1
      },
      emphasis: {
        itemStyle: {
          areaColor: '#2a333d'
        }
      }
    },
    series: [
      {
        name: '公司数量',
        type: 'map',
        map: 'world',
        geoIndex: 0,
        data: Object.entries(countryStats).map(([country, count]) => ({
          name: country,
          value: count
        }))
      }
    ]
  };

  // 技术路线标签颜色
  const techColors: Record<string, string> = {
    'Tokamak': 'blue',
    'Stellarator': 'purple',
    'Magnetized Target Fusion': 'green',
    'Field-Reversed Configuration': 'orange',
    'Inertial Confinement Fusion': 'red',
    'Laser-Driven Fusion': 'cyan',
    'Sheared-Flow Stabilized Z-Pinch': 'gold',
    'Spherical Tokamak': 'geekblue',
    'Inertial Electrostatic Confinement': 'lime',
    'Helical Reactor': 'magenta',
    'Alternative Concepts': 'volcano'
  };

  const columns = [
    {
      title: '公司名称',
      dataIndex: 'name',
      key: 'name',
      fixed: 'left',
      width: 250,
      render: (text: string, record: Company) => (
        <a href={record.website} target="_blank" rel="noopener noreferrer">
          {text}
        </a>
      )
    },
    {
      title: '国家',
      dataIndex: 'country',
      key: 'country',
      width: 150
    },
    {
      title: '成立年份',
      dataIndex: 'founded_year',
      key: 'founded_year',
      width: 100,
      sorter: (a: Company, b: Company) => a.founded_year - b.founded_year
    },
    {
      title: '技术路线',
      dataIndex: 'technology_type',
      key: 'technology_type',
      width: 200,
      render: (tech: string) => (
        <Tag color={techColors[tech] || 'default'}>
          {tech}
        </Tag>
      )
    },
    {
      title: '简介',
      dataIndex: 'description',
      key: 'description',
      ellipsis: true
    }
  ];

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '40px' }}>
        <Spin size="large" tip="加载公司数据..." />
      </div>
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* 地图 */}
      <Card>
        <ReactECharts option={mapOption} style={{ height: '500px' }} />
      </Card>

      {/* 公司列表 */}
      <Card title={`核聚变公司列表 (${companies.length}家)`}>
        <Table
          columns={columns}
          dataSource={companies}
          rowKey="id"
          pagination={{ pageSize: 10 }}
          scroll={{ x: 1200 }}
          size="middle"
        />
      </Card>

      {/* 统计信息 */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px' }}>
        <Card size="small" title="公司总数">
          <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#1890ff' }}>
            {companies.length}
          </div>
        </Card>
        <Card size="small" title="覆盖国家">
          <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#52c41a' }}>
            {Object.keys(countryStats).length}
          </div>
        </Card>
        <Card size="small" title="技术路线">
          <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#faad14' }}>
            {new Set(companies.map(c => c.technology_type)).size}
          </div>
        </Card>
        <Card size="small" title="平均成立年限">
          <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#f5222d' }}>
            {Math.round(companies.reduce((acc, c) => acc + (2026 - c.founded_year), 0) / companies.length)} 年
          </div>
        </Card>
      </div>
    </div>
  );
};

export default CompanyMap;
