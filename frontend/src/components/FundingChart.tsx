/**
 * 融资数据可视化组件
 * 展示融资趋势、按技术路线分布、按国家分布
 */

import React, { useEffect, useState } from 'react';
import ReactECharts from 'echarts-for-react';
import { Card, Spin, Empty } from 'antd';
import axios from 'axios';

interface FundingStats {
  total_funding: number;
  total_rounds: number;
  avg_round_size: number;
  median_round_size: number;
  largest_round: number;
}

interface TimelineData {
  year: number;
  month: number;
  total_funding: number;
  total_rounds: number;
}

interface TechDistribution {
  [key: string]: {
    total_funding: number;
    total_rounds: number;
  };
}

const API_BASE = '/api/v1';

const FundingChart: React.FC = () => {
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<FundingStats | null>(null);
  const [timeline, setTimeline] = useState<TimelineData[]>([]);
  const [techDist, setTechDist] = useState<TechDistribution>({});

  useEffect(() => {
    fetchFundingData();
  }, []);

  const fetchFundingData = async () => {
    try {
      setLoading(true);
      const [statsRes, timelineRes, techRes] = await Promise.all([
        axios.get(`${API_BASE}/funding/stats`),
        axios.get(`${API_BASE}/funding/stats/timeline?start_year=2020&end_year=2026`),
        axios.get(`${API_BASE}/funding/stats/by-technology`)
      ]);
      
      setStats(statsRes.data);
      setTimeline(timelineRes.data);
      setTechDist(techRes.data);
    } catch (error) {
      console.error('Failed to fetch funding data:', error);
    } finally {
      setLoading(false);
    }
  };

  // 融资趋势图配置
  const trendOption = {
    title: {
      text: '全球核聚变融资趋势',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      formatter: (params: any) => {
        const data = params[0];
        const funding = data.value[1] / 1_000_000;
        const rounds = data.value[2];
        return `${data.name}<br/>融资金额：$${funding.toFixed(0)}M<br/>融资轮次：${rounds}`;
      }
    },
    xAxis: {
      type: 'category',
      data: timeline.map(d => `${d.year}-${String(d.month).padStart(2, '0')}`),
      axisLabel: {
        rotate: 45,
        interval: Math.floor(timeline.length / 12)
      }
    },
    yAxis: [
      {
        type: 'value',
        name: '融资金额 (百万美元)',
        axisLabel: {
          formatter: (value: number) => `$${value}M`
        }
      },
      {
        type: 'value',
        name: '融资轮次',
        axisLabel: {
          formatter: (value: number) => `${value}`
        }
      }
    ],
    series: [
      {
        name: '融资金额',
        type: 'bar',
        data: timeline.map(d => [
          `${d.year}-${String(d.month).padStart(2, '0')}`,
          d.total_funding / 1_000_000,
          d.total_rounds
        ]),
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
            { offset: 0, color: '#83bff6' },
            { offset: 1, color: '#188df0' }
          ])
        }
      },
      {
        name: '融资轮次',
        type: 'line',
        yAxisIndex: 1,
        data: timeline.map(d => d.total_rounds),
        itemStyle: {
          color: '#ff6b6b'
        },
        smooth: true
      }
    ]
  };

  // 技术路线分布图配置
  const techOption = {
    title: {
      text: '按技术路线融资分布',
      left: 'center'
    },
    tooltip: {
      trigger: 'item',
      formatter: (params: any) => {
        const data = techDist[params.name];
        const funding = data ? data.total_funding / 1_000_000 : 0;
        return `${params.name}<br/>总金额：$${funding.toFixed(0)}M<br/>轮次数：${data?.total_rounds || 0}`;
      }
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '融资金额',
        type: 'pie',
        radius: '60%',
        data: Object.entries(techDist).map(([name, data]) => ({
          name,
          value: data.total_funding / 1_000_000
        })),
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowOffsetX: 0,
            shadowColor: 'rgba(0, 0, 0, 0.5)'
          }
        },
        label: {
          formatter: '{b}: ${c}M'
        }
      }
    ]
  };

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: '40px' }}>
        <Spin size="large" tip="加载融资数据..." />
      </div>
    );
  }

  if (!stats) {
    return (
      <Empty description="暂无融资数据" />
    );
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
      {/* 统计卡片 */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px' }}>
        <Card size="small" title="总融资金额">
          <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#1890ff' }}>
            ${(stats.total_funding / 1_000_000_000).toFixed(2)}B
          </div>
        </Card>
        <Card size="small" title="融资轮次总数">
          <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#52c41a' }}>
            {stats.total_rounds}
          </div>
        </Card>
        <Card size="small" title="平均轮次金额">
          <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#faad14' }}>
            ${(stats.avg_round_size / 1_000_000).toFixed(1)}M
          </div>
        </Card>
        <Card size="small" title="最大单笔融资">
          <div style={{ fontSize: '24px', fontWeight: 'bold', color: '#f5222d' }}>
            ${(stats.largest_round / 1_000_000_000).toFixed(2)}B
          </div>
        </Card>
      </div>

      {/* 融资趋势图 */}
      <Card>
        <ReactECharts option={trendOption} style={{ height: '400px' }} />
      </Card>

      {/* 技术路线分布 */}
      <Card>
        <ReactECharts option={techOption} style={{ height: '400px' }} />
      </Card>
    </div>
  );
};

export default FundingChart;
