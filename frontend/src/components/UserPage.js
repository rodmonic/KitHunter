// App.js
import React, { useState } from 'react';
import DataExplorer from './DataExplorer';


import { Layout, Menu } from 'antd';
import {
  MenuUnfoldOutlined,
  MenuFoldOutlined,
  UserOutlined,
  SearchOutlined,
  SkinOutlined,
} from '@ant-design/icons';

const { Header, Sider, Content } = Layout;
// const { Panel } = Collapse;

const App = () => {
  const [collapsed, setCollapsed] = useState(false);
  const [selectedMenu, setSelectedMenu] = useState('1'); // Track selected menu item
  const [selectedCountry, setSelectedCountry] = useState(null); // Track selected country

  const toggle = () => {
    setCollapsed(!collapsed);
  };

  const handleMenuClick = (e) => {
    setSelectedMenu(e.key);
    setSelectedCountry(null);
  };

  const handleCountryClick = (country) => {
    setSelectedCountry(selectedCountry === country ? null : country); // Toggle country selection
  };

  // Define content for each menu item
  const renderContent = () => {
    switch (selectedMenu) {
      case '1':
        return <div>Home Content</div>;
      case '2':
        return <div>About Content</div>;
      case '3':
        return <div><DataExplorer /></div>;
      default:
        return <div>Home Content</div>;
    }
  };

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider trigger={null} collapsible collapsed={collapsed}>
        <div className="logo" />
        <Menu
          theme="dark"
          mode="inline"
          defaultSelectedKeys={['1']}
          onClick={handleMenuClick}
        >
          <Menu.Item key="1" icon={<UserOutlined />}>
            Home
          </Menu.Item>
          <Menu.Item key="2" icon={<SkinOutlined />}>
            Hunt
          </Menu.Item>
          <Menu.Item key="3" icon={<SearchOutlined />}>
            Search
          </Menu.Item>
        </Menu>
      </Sider>
      <Layout>
        <Header
          style={{
            padding: 0,
            background: '#001529',
            color: '#fff',
            textAlign: 'center',
          }}
        >
          {React.createElement(
            collapsed ? MenuUnfoldOutlined : MenuFoldOutlined,
            {
              className: 'trigger',
              onClick: toggle,
            }
          )}
          Kit Hunter
        </Header>
        <Content
          style={{
            margin: '24px 16px',
            padding: 24,
            background: '#fff',
            minHeight: 280,
            maxHeight: 'calc(100vh - 64px - 48px)',
            overflowY: 'auto'
          }}
        >
          {renderContent()}
        </Content>
      </Layout>
    </Layout>
  );
};

export default App;
