// API基础URL
const API_BASE_URL = 'http://localhost:8000/api';

// DOM元素
const elements = {
    sidebar: document.querySelector('.admin-sidebar'),
    sidebarToggle: document.getElementById('sidebar-toggle'),
    pageTitle: document.getElementById('page-title'),
    contentPages: {
        dashboard: document.getElementById('dashboard-page'),
        users: document.getElementById('users-page'),
        settings: document.getElementById('settings-page'),
        logs: document.getElementById('logs-page')
    },
    navItems: document.querySelectorAll('.nav-item'),
    logoutBtn: document.getElementById('logout-btn'),
    userId: document.getElementById('user-id'),
    totalUsers: document.getElementById('total-users'),
    cpuUsage: document.getElementById('cpu-usage'),
    memoryUsage: document.getElementById('memory-usage'),
    diskUsage: document.getElementById('disk-usage'),
    serverTime: document.getElementById('server-time'),
    usersTableBody: document.getElementById('users-table-body'),
    userSearch: document.getElementById('user-search'),
    addUserBtn: document.getElementById('add-user-btn'),
    userModal: document.getElementById('user-modal'),
    modalTitle: document.getElementById('modal-title'),
    userForm: document.getElementById('user-form'),
    userUsername: document.getElementById('user-username'),
    userRealname: document.getElementById('user-realname'),
    userEmail: document.getElementById('user-email'),
    userPassword: document.getElementById('user-password'),
    userPhone: document.getElementById('user-phone'),
    confirmModal: document.getElementById('confirm-modal'),
    confirmTitle: document.getElementById('confirm-title'),
    confirmMessage: document.getElementById('confirm-message'),
    confirmOk: document.getElementById('confirm-ok'),
    confirmCancel: document.getElementById('confirm-cancel'),
    loadingOverlay: document.getElementById('loading-overlay'),
    notification: document.getElementById('notification'),
    notificationIcon: document.querySelector('.notification-icon'),
    notificationMessage: document.querySelector('.notification-message')
};

// 当前操作的用户ID
let currentUserId = null;

// 确认操作回调
let confirmCallback = null;

// 初始化
function init() {
    // 绑定事件
    bindEvents();
    
    // 初始化侧边栏状态
    const adminContent = document.querySelector('.admin-content');
    const isCollapsed = elements.sidebar.classList.contains('collapsed');
    if (isCollapsed) {
        adminContent.style.marginLeft = '70px';
    }
    
    // 加载仪表盘数据
    loadDashboardData();
    
    // 设置服务器时间
    updateServerTime();
    setInterval(updateServerTime, 1000);
}

// 绑定事件
function bindEvents() {
    // 侧边栏切换
    elements.sidebarToggle.addEventListener('click', toggleSidebar);
    
    // 导航项点击
    elements.navItems.forEach(item => {
        item.addEventListener('click', (e) => {
            e.preventDefault();
            const page = item.dataset.page;
            switchPage(page);
        });
    });
    
    // 返回桌面
    elements.logoutBtn.addEventListener('click', backToDesktop);
    
    // 用户管理事件
    elements.addUserBtn.addEventListener('click', () => openUserModal());
    elements.userSearch.addEventListener('input', debounce(searchUsers, 300));
    
    // 表单提交
    elements.userForm.addEventListener('submit', handleUserFormSubmit);
    
    // 模态框关闭
    document.querySelectorAll('.modal .delete, .modal .modal-close').forEach(btn => {
        btn.addEventListener('click', closeModals);
    });
    
    // 确认模态框
    elements.confirmCancel.addEventListener('click', closeModals);
    elements.confirmOk.addEventListener('click', handleConfirm);
    
    // 密码显示/隐藏
    document.querySelectorAll('.toggle-password').forEach(btn => {
        btn.addEventListener('click', togglePassword);
    });
    
    // 通知关闭
    document.querySelector('.notification .delete').addEventListener('click', hideNotification);
}

// 切换侧边栏
function toggleSidebar() {
    const isCollapsed = elements.sidebar.classList.toggle('collapsed');
    const adminContent = document.querySelector('.admin-content');
    if (isCollapsed) {
        adminContent.style.marginLeft = '70px';
    } else {
        adminContent.style.marginLeft = '280px';
    }
}

// 切换页面
function switchPage(page) {
    // 更新导航项状态
    elements.navItems.forEach(item => {
        item.classList.remove('active');
        if (item.dataset.page === page) {
            item.classList.add('active');
        }
    });
    
    // 更新页面标题
    elements.pageTitle.textContent = getPageTitle(page);
    
    // 显示对应页面
    Object.keys(elements.contentPages).forEach(key => {
        elements.contentPages[key].style.display = key === page ? 'block' : 'none';
    });
    
    // 加载页面数据
    switch (page) {
        case 'dashboard':
            loadDashboardData();
            break;
        case 'users':
            loadUsers();
            break;
        case 'logs':
            loadLogs();
            break;
    }
}

// 获取页面标题
function getPageTitle(page) {
    const titles = {
        dashboard: '仪表盘',
        users: '用户管理',
        settings: '系统设置',
        logs: '系统日志'
    };
    return titles[page] || '仪表盘';
}

// 加载仪表盘数据
async function loadDashboardData() {
    try {
        showLoading();
        
        // 获取系统状态
        try {
            const systemStatusUrl = 'http://localhost:8000/api/system/status/public';
            console.log('直接请求系统状态:', systemStatusUrl);
            const systemResponse = await fetch(systemStatusUrl);
            console.log('系统状态响应:', systemResponse.status);
            if (systemResponse.ok) {
                const systemStatus = await systemResponse.json();
                console.log('系统状态数据:', systemStatus);
                if (systemStatus && systemStatus.code === 200) {
                    const data = systemStatus.data;
                    elements.cpuUsage.textContent = `${data.cpu_usage}%`;
                    elements.memoryUsage.textContent = `${data.memory_usage}%`;
                    elements.diskUsage.textContent = `${data.disk_usage}%`;
                }
            }
        } catch (error) {
            console.error('获取系统状态失败:', error);
            // 保持默认值
        }
        
        // 获取用户总数
        try {
            const usersUrl = 'http://localhost:8000/api/admin/users';
            console.log('直接请求用户数据:', usersUrl);
            const usersResponse = await fetch(usersUrl, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            });
            console.log('用户数据响应:', usersResponse.status);
            if (usersResponse.ok) {
                const usersData = await usersResponse.json();
                console.log('用户数据:', usersData);
                if (usersData && usersData.code === 200) {
                    const total = usersData.data.total;
                    elements.totalUsers.textContent = total;
                }
            }
        } catch (error) {
            console.error('获取用户总数失败:', error);
            // 保持默认值
        }
        
    } catch (error) {
        showNotification('加载仪表盘数据失败', 'error');
        console.error('加载仪表盘数据失败:', error);
    } finally {
        hideLoading();
    }
}

// 加载用户列表
async function loadUsers() {
    try {
        showLoading();
        
        const response = await fetchData('/admin/users');
        if (response && response.code === 200) {
            const users = response.data.users;
            renderUsersTable(users);
        } else {
            renderUsersTable([]);
        }
    } catch (error) {
        showNotification('加载用户数据失败', 'error');
        console.error('加载用户数据失败:', error);
        renderUsersTable([]);
    } finally {
        hideLoading();
    }
}

// 渲染用户表格
function renderUsersTable(users) {
    if (users.length === 0) {
        elements.usersTableBody.innerHTML = `
            <tr>
                <td colspan="6" class="has-text-centered">
                    <p>暂无用户数据</p>
                </td>
            </tr>
        `;
        return;
    }
    
    elements.usersTableBody.innerHTML = users.map(user => `
        <tr>
            <td>${user.user_id}</td>
            <td>${user.username}</td>
            <td>${user.realname}</td>
            <td>${user.email || '-'}</td>
            <td>${user.phone || '-'}</td>
            <td>
                <div class="actions">
                    <button class="edit-btn" onclick="editUser(${user.user_id})">
                        <i class="fas fa-edit"></i>
                        <span>编辑</span>
                    </button>
                    <button class="delete-btn" onclick="deleteUser(${user.user_id}, '${user.username}')">
                        <i class="fas fa-trash"></i>
                        <span>删除</span>
                    </button>
                </div>
            </td>
        </tr>
    `).join('');
}

// 搜索用户
async function searchUsers() {
    const searchTerm = elements.userSearch.value.toLowerCase();
    if (!searchTerm) {
        loadUsers();
        return;
    }
    
    try {
        showLoading();
        const response = await fetchData('/admin/users');
        if (response && response.code === 200) {
            const users = response.data.users.filter(user => 
                user.username.toLowerCase().includes(searchTerm) ||
                user.realname.toLowerCase().includes(searchTerm) ||
                user.email?.toLowerCase().includes(searchTerm) ||
                user.phone?.includes(searchTerm)
            );
            renderUsersTable(users);
        }
    } catch (error) {
        console.error('搜索用户失败:', error);
        renderUsersTable([]);
    } finally {
        hideLoading();
    }
}

// 打开用户模态框
function openUserModal(userId = null) {
    currentUserId = userId;
    
    if (userId) {
        // 编辑模式
        elements.modalTitle.textContent = '编辑用户';
        loadUserDetails(userId);
    } else {
        // 添加模式
        elements.modalTitle.textContent = '添加用户';
        resetUserForm();
    }
    
    elements.userModal.classList.add('is-active');
}

// 加载用户详情
async function loadUserDetails(userId) {
    try {
        showLoading();
        const response = await fetchData(`/admin/users/${userId}`);
        if (response && response.code === 200) {
            const user = response.data;
            elements.userUsername.value = user.username;
            elements.userRealname.value = user.realname;
            elements.userEmail.value = user.email || '';
            elements.userPhone.value = user.phone || '';
            elements.userId.value = userId;
        }
    } catch (error) {
        showNotification('加载用户详情失败', 'error');
        console.error('加载用户详情失败:', error);
    } finally {
        hideLoading();
    }
}

// 重置用户表单
function resetUserForm() {
    elements.userForm.reset();
    elements.userId.value = '';
    elements.userPassword.value = '';
    // 清除错误消息
    document.querySelectorAll('.error-message').forEach(el => el.textContent = '');
}

// 处理用户表单提交
async function handleUserFormSubmit(e) {
    e.preventDefault();
    
    try {
        showLoading();
        
        const userData = {
            username: elements.userUsername.value.trim(),
            realname: elements.userRealname.value.trim(),
            email: elements.userEmail.value.trim() || null,
            phone: elements.userPhone.value.trim() || null
        };
        
        // 如果填写了密码，则添加到数据中
        if (elements.userPassword.value) {
            userData.password = elements.userPassword.value;
        }
        
        let response;
        if (elements.userId.value) {
            // 更新用户
            response = await fetchData(`/admin/users/${elements.userId.value}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            });
        } else {
            // 添加用户
            response = await fetchData('/auth/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(userData)
            });
        }
        
        if (response && response.code === 200) {
            showNotification(elements.userId.value ? '用户更新成功' : '用户添加成功', 'success');
            closeModals();
            loadUsers();
        } else {
            showNotification('操作失败', 'error');
        }
    } catch (error) {
        showNotification('操作失败: ' + (error.message || '未知错误'), 'error');
        console.error('处理用户表单失败:', error);
    } finally {
        hideLoading();
    }
}

// 编辑用户
function editUser(userId) {
    openUserModal(userId);
}

// 删除用户
function deleteUser(userId, username) {
    elements.confirmTitle.textContent = '删除用户';
    elements.confirmMessage.textContent = `您确定要删除用户 "${username}" 吗？此操作不可恢复。`;
    elements.confirmModal.classList.add('is-active');
    
    confirmCallback = async () => {
        try {
            showLoading();
            const response = await fetchData(`/admin/users/${userId}`, {
                method: 'DELETE'
            });
            
            if (response && response.code === 200) {
                showNotification('用户删除成功', 'success');
                loadUsers();
            } else {
                showNotification('删除失败', 'error');
            }
        } catch (error) {
            showNotification('删除失败: ' + (error.message || '未知错误'), 'error');
            console.error('删除用户失败:', error);
        } finally {
            hideLoading();
            closeModals();
        }
    };
}

// 处理确认操作
function handleConfirm() {
    if (confirmCallback) {
        confirmCallback();
        confirmCallback = null;
    }
}

// 关闭所有模态框
function closeModals() {
    elements.userModal.classList.remove('is-active');
    elements.confirmModal.classList.remove('is-active');
    confirmCallback = null;
}

// 加载系统日志
async function loadLogs() {
    try {
        showLoading();
        
        // 模拟日志数据
        const logs = [
            { time: '2026-02-14 19:30:00', level: 'info', message: '系统启动' },
            { time: '2026-02-14 19:25:00', level: 'info', message: '用户 admin 登录成功' },
            { time: '2026-02-14 19:20:00', level: 'warning', message: '内存使用率超过80%' },
            { time: '2026-02-14 19:15:00', level: 'error', message: '数据库连接失败' },
            { time: '2026-02-14 19:10:00', level: 'info', message: '系统状态检查' },
            { time: '2026-02-14 19:05:00', level: 'critical', message: 'CPU使用率超过95%' }
        ];
        
        setTimeout(() => {
            const logsContent = document.getElementById('logs-content');
            logsContent.innerHTML = logs.map(log => `
                <div class="log-entry ${log.level}">
                    <span class="log-time">${log.time}</span>
                    <span class="log-level">${log.level.toUpperCase()}</span>
                    <span class="log-message">${log.message}</span>
                </div>
            `).join('');
            hideLoading();
        }, 500);
        
    } catch (error) {
        showNotification('加载日志失败', 'error');
        console.error('加载日志失败:', error);
        hideLoading();
    }
}

// 更新服务器时间
function updateServerTime() {
    const now = new Date();
    elements.serverTime.textContent = now.toLocaleString('zh-CN');
}

// 返回桌面
function backToDesktop() {
    elements.confirmTitle.textContent = '返回桌面';
    elements.confirmMessage.textContent = '您确定要返回桌面吗？';
    elements.confirmModal.classList.add('is-active');
    
    confirmCallback = () => {
        // 跳转到ClassNet主页面（桌面）
        window.location.href = 'http://localhost:8000/frontend/desktop/index.html';
    };
}

// 显示通知
function showNotification(message, type = 'info') {
    elements.notificationMessage.textContent = message;
    elements.notification.className = `notification ${type} show`;
    
    // 设置图标
    const icons = {
        success: 'fas fa-check-circle',
        error: 'fas fa-exclamation-circle',
        warning: 'fas fa-exclamation-triangle',
        info: 'fas fa-info-circle'
    };
    elements.notificationIcon.className = icons[type] || icons.info;
    
    // 3秒后自动隐藏
    setTimeout(() => {
        hideNotification();
    }, 3000);
}

// 隐藏通知
function hideNotification() {
    elements.notification.classList.remove('show');
}

// 显示加载遮罩
function showLoading() {
    elements.loadingOverlay.classList.add('active');
}

// 隐藏加载遮罩
function hideLoading() {
    elements.loadingOverlay.classList.remove('active');
}

// 切换密码显示/隐藏
function togglePassword(e) {
    const button = e.target.closest('.toggle-password');
    const input = button.previousElementSibling;
    const icon = button.querySelector('i');
    
    if (input.type === 'password') {
        input.type = 'text';
        icon.className = 'fas fa-eye-slash';
    } else {
        input.type = 'password';
        icon.className = 'fas fa-eye';
    }
}

// 发送API请求
async function fetchData(endpoint, options = {}) {
    try {
        // 添加认证令牌
        const token = localStorage.getItem('token');
        if (token) {
            options.headers = {
                ...options.headers,
                'Authorization': `Bearer ${token}`
            };
        }
        
        const url = `${API_BASE_URL}${endpoint}`;
        console.log('API请求URL:', url);
        console.log('API请求选项:', options);
        const response = await fetch(url, options);
        
        console.log('API响应状态:', response.status);
        console.log('API响应头:', Object.fromEntries(response.headers));
        
        if (!response.ok) {
            // 尝试获取错误信息
            try {
                const errorText = await response.text();
                console.log('API错误响应:', errorText);
                throw new Error(`请求失败: ${response.status}, ${errorText}`);
            } catch (e) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
        }
        
        return await response.json();
    } catch (error) {
        console.error('API请求失败:', error);
        throw error;
    }
}

// 防抖函数
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// 检查登录状态
function checkLoginStatus() {
    const token = localStorage.getItem('token');
    if (!token) {
        // 未登录，跳转到登录页面
        console.log('未登录，跳转到登录页面');
        window.location.href = '../../auth/index.html';
        return false;
    }
    console.log('已登录，token:', token);
    return true;
}

// 初始化
console.log('开始初始化');
if (checkLoginStatus()) {
    console.log('登录状态检查通过，开始初始化应用');
    init();
}

// 全局函数
window.editUser = editUser;
window.deleteUser = deleteUser;
window.handleConfirm = handleConfirm;
window.togglePassword = togglePassword;
