// 桌面页面脚本

// 预加载壁纸图片
function preloadWallpaper() {
    var wallpaper = new Image();
    wallpaper.src = '../public/images/wallpaper.png';
    wallpaper.onload = function() {
        // 图片加载完成后，添加到body
        document.body.classList.add('wallpaper-loaded');
    };
    // 即使图片加载失败，也确保页面正常显示
    wallpaper.onerror = function() {
        document.body.classList.add('wallpaper-loaded');
    };
}

// 立即开始预加载壁纸
preloadWallpaper();

// DOM 加载完成后执行
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initDesktop);
} else {
    initDesktop();
}

function initDesktop() {
    // 初始化Dock栏
    initDock();
    // 初始化通知栏
    initNotificationBar();
}

// 初始化侧边栏切换功能
function initSidebarToggle() {
    var sidebarToggle = document.querySelector('.sidebar-toggle');
    var sidebar = document.querySelector('.sidebar');
    
    if (sidebarToggle && sidebar) {
        // 初始状态：侧边栏展开
        sidebar.classList.remove('collapsed');
        
        sidebarToggle.addEventListener('click', function() {
            sidebar.classList.toggle('collapsed');
        });
        
        // 一段时间无操作后自动缩小侧边栏
        initAutoCollapseSidebar(sidebar);
    }
}

// 初始化侧边栏自动缩小功能
function initAutoCollapseSidebar(sidebar) {
    var inactivityTimer;
    var inactivityThreshold = 30000; // 30秒无操作
    
    // 重置无操作计时器
    function resetInactivityTimer() {
        clearTimeout(inactivityTimer);
        inactivityTimer = setTimeout(function() {
            if (!sidebar.classList.contains('collapsed')) {
                sidebar.classList.add('collapsed');
            }
        }, inactivityThreshold);
    }
    
    // 监听用户操作
    document.addEventListener('mousemove', resetInactivityTimer);
    document.addEventListener('keydown', resetInactivityTimer);
    document.addEventListener('click', resetInactivityTimer);
    document.addEventListener('scroll', resetInactivityTimer);
    
    // 初始启动计时器
    resetInactivityTimer();
}

// 初始化用户菜单切换功能
function initUserMenuToggle() {
    var userProfile = document.querySelector('.user-profile');
    var userMenu = document.getElementById('user-menu');
    
    if (userProfile && userMenu) {
        userProfile.addEventListener('click', function(e) {
            e.stopPropagation();
            userMenu.classList.toggle('active');
        });
        
        // 点击外部关闭用户菜单
        document.addEventListener('click', function(e) {
            if (!userProfile.contains(e.target) && !userMenu.contains(e.target)) {
                userMenu.classList.remove('active');
            }
        });
    }
}

// 初始化应用卡片点击功能
function initAppCards() {
    var appCards = document.querySelectorAll('.app-card');
    
    if (appCards.length > 0) {
        appCards.forEach(function(card) {
            card.addEventListener('click', function() {
                launchApp(card);
            });
        });
    }
}

// 工具函数：使用requestAnimationFrame实现延迟
function delay(ms, callback) {
    var start = Date.now();
    function tick() {
        var now = Date.now();
        if (now - start >= ms) {
            callback();
        } else {
            requestAnimationFrame(tick);
        }
    }
    requestAnimationFrame(tick);
}

// 启动应用
function launchApp(card) {
    var appName = card.querySelector('.app-name').textContent;
    console.log('启动应用:', appName);
    
    // 添加入场动画
    card.classList.add('launching');
    delay(500, function() {
        card.classList.remove('launching');
    });
    
    // 根据应用名称跳转到对应页面
    switch (appName) {
        case '视频播放器':
            window.location.href = '../apps/video/index.html';
            break;
        case '音乐播放器':
            window.location.href = '../apps/music/index.html';
            break;
        case '天气':
            window.location.href = '../apps/weather/index.html';
            break;
        case '聊天':
            window.location.href = '../apps/chat/index.html';
            break;
        case '日历':
            window.location.href = '../apps/calendar/index.html';
            break;
        case '课程表':
            window.location.href = '../apps/schedule/index.html';
            break;
        default:
            console.log('应用未找到:', appName);
    }
}

// 初始化用户信息
function initUserInfo() {
    // 从本地存储获取用户信息
    var user = localStorage.getItem('user');
    if (user) {
        try {
            user = JSON.parse(user);
            updateUserInfo(user);
        } catch (e) {
            console.error('解析用户信息失败:', e);
            // 模拟用户信息
            simulateUserInfo();
        }
    } else {
        // 模拟用户信息
        simulateUserInfo();
    }
}

// 更新用户信息
function updateUserInfo(user) {
    var userNameElement = document.getElementById('user-name');
    var userEmailElement = document.getElementById('user-email');
    var userAvatarElement = document.getElementById('user-avatar');
    
    if (userNameElement) {
        userNameElement.textContent = user.username || '用户名';
    }
    
    if (userEmailElement) {
        userEmailElement.textContent = user.email || 'user@example.com';
    }
    
    if (userAvatarElement) {
        generateUserAvatar(user.username || '用户');
    }
}

// 模拟用户信息
function simulateUserInfo() {
    var user = {
        username: '张三',
        email: 'zhangsan@example.com'
    };
    updateUserInfo(user);
}

// 生成用户头像
function generateUserAvatar(name) {
    var avatar = document.getElementById('user-avatar');
    if (name && avatar) {
        var initials = name.split(' ')
            .map(function(word) { return word[0]; })
            .join('')
            .toUpperCase()
            .slice(0, 2);
        avatar.textContent = initials;
        
        // 生成随机背景色
        var colors = ['#3B82F6', '#10B981', '#F59E0B', '#EF4444', '#8B5CF6'];
        var randomColor = colors[Math.floor(Math.random() * colors.length)];
        avatar.style.backgroundColor = randomColor;
    }
}

// 初始化退出登录功能
function initLogout() {
    var logoutBtn = document.getElementById('logout-btn');
    
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            handleLogout();
        });
    }
}

// 处理退出登录
function handleLogout() {
    // 清除本地存储
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    
    // 跳转到登录页面
    window.location.href = '../auth/index.html';
}

// 工具函数：获取元素
function getElementById(id) {
    return document.getElementById(id);
}

// 工具函数：添加事件监听器
function addEventListener(element, event, callback) {
    if (element && element.addEventListener) {
        element.addEventListener(event, callback);
    } else if (element && element.attachEvent) {
        // 兼容旧IE
        element.attachEvent('on' + event, callback);
    }
}

// 工具函数：检查元素是否包含类
function hasClass(element, className) {
    if (element.classList) {
        return element.classList.contains(className);
    } else {
        // 兼容旧IE
        return new RegExp('\\b' + className + '\\b').test(element.className);
    }
}

// 工具函数：添加类
function addClass(element, className) {
    if (element.classList) {
        element.classList.add(className);
    } else {
        // 兼容旧IE
        if (!hasClass(element, className)) {
            element.className += ' ' + className;
        }
    }
}

// 工具函数：移除类
function removeClass(element, className) {
    if (element.classList) {
        element.classList.remove(className);
    } else {
        // 兼容旧IE
        element.className = element.className.replace(new RegExp('\\b' + className + '\\b', 'g'), '').trim();
    }
}

// 工具函数：切换类
function toggleClass(element, className) {
    if (element.classList) {
        element.classList.toggle(className);
    } else {
        // 兼容旧IE
        if (hasClass(element, className)) {
            removeClass(element, className);
        } else {
            addClass(element, className);
        }
    }
}

// 初始化Dock栏功能
function initDock() {
    var dockItems = document.querySelectorAll('.dock-item');
    
    if (dockItems.length > 0) {
        dockItems.forEach(function(item) {
            item.addEventListener('click', function() {
                var app = this.getAttribute('data-app');
                launchAppFromDock(app);
            });
        });
    }
}

// 从Dock栏启动应用
function launchAppFromDock(app) {
    console.log('从Dock栏启动应用:', app);
    
    // 添加入场动画
    var dockItem = document.querySelector('.dock-item[data-app="' + app + '"]');
    if (dockItem) {
        dockItem.classList.add('launching');
        delay(500, function() {
            dockItem.classList.remove('launching');
        });
    }
    
    // 根据应用名称跳转到对应页面
    switch (app) {

        case 'video':
            window.location.href = '../apps/video/index.html';
            break;
        case 'music':
            window.location.href = '../apps/music/index.html';
            break;
        case 'weather':
            window.location.href = '../apps/weather/index.html';
            break;
        case 'chat':
            window.location.href = '../apps/chat/index.html';
            break;
        case 'calendar':
            window.location.href = '../apps/calendar/index.html';
            break;
        case 'schedule':
            window.location.href = '../apps/schedule/index.html';
            break;
        case 'settings':
            window.location.href = '../settings/index.html';
            break;
        default:
            console.log('应用未找到:', app);
    }
}

// 初始化通知栏
function initNotificationBar() {
    // 初始化用户信息
    initUserInfo();
    
    // 初始化消息广播接口
    initBroadcastSystem();
}

// 初始化消息广播系统
function initBroadcastSystem() {
    // 预留消息广播接口，用于后续通过管理后台进行消息广播
    // 这里可以添加一个从服务器获取广播消息的函数
    // 示例：
    // fetchBroadcastMessage();
    
    // 每60秒检查一次是否有新的广播消息
    // setInterval(fetchBroadcastMessage, 60000);
}

// 更新欢迎文本（预留接口，供管理后台调用）
function updateWelcomeText(mainText, subText) {
    var welcomeMain = document.querySelector('.welcome-main');
    var welcomeSub = document.querySelector('.welcome-sub');
    
    if (welcomeMain && mainText) {
        welcomeMain.textContent = mainText;
    }
    
    if (welcomeSub && subText) {
        welcomeSub.textContent = subText;
    }
}

// 获取广播消息（预留接口，供后续实现）
function fetchBroadcastMessage() {
    // 这里可以实现从服务器获取广播消息的逻辑
    // 示例：
    /*
    fetch('../api/broadcast')
        .then(response => response.json())
        .then(data => {
            if (data.mainText || data.subText) {
                updateWelcomeText(data.mainText, data.subText);
            }
        })
        .catch(error => {
            console.error('获取广播消息失败:', error);
        });
    */
}