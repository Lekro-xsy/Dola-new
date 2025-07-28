// 应用程序状态
let currentImageIndex = 1;
let totalImages = 100;
let imageData = {};

// DOM元素
const normalImageContainer = document.getElementById('normalImageContainer');
const dolaImageContainer = document.getElementById('dolaImageContainer');
const promptText = document.getElementById('promptText');
const currentIndexElement = document.getElementById('currentIndex');
const totalImagesElement = document.getElementById('totalImages');
const imageSelector = document.getElementById('imageSelector');

// 分数元素
const normalScores = {
    color: document.getElementById('normalColorScore'),
    spatial: document.getElementById('normalSpatialScore'),
    count: document.getElementById('normalCountScore'),
    relevance: document.getElementById('normalRelevanceScore'),
    overall: document.getElementById('normalOverallScore')
};

const dolaScores = {
    color: document.getElementById('dolaColorScore'),
    spatial: document.getElementById('dolaSpatialScore'),
    count: document.getElementById('dolaCountScore'),
    relevance: document.getElementById('dolaRelevanceScore'),
    overall: document.getElementById('dolaOverallScore')
};

// 初始化应用
async function initApp() {
    try {
        // 加载数据
        const response = await fetch('data.json');
        imageData = await response.json();
        
        // 设置总图片数量
        totalImages = Object.keys(imageData).length;
        totalImagesElement.textContent = totalImages;
        
        // 初始化图片选择器
        initImageSelector();
        
        // 显示第一张图片
        showImage(1);
        
    } catch (error) {
        console.error('Failed to load data:', error);
        showError('数据加载失败');
    }
}

// 初始化图片选择器
function initImageSelector() {
    imageSelector.innerHTML = '';
    for (let i = 1; i <= totalImages; i++) {
        const option = document.createElement('option');
        option.value = i;
        option.textContent = `图片 ${i}`;
        imageSelector.appendChild(option);
    }
}

// 显示图片和数据
function showImage(index) {
    if (!imageData[index]) {
        showError('图片数据不存在');
        return;
    }
    
    currentImageIndex = index;
    const data = imageData[index];
    
    // 更新当前索引显示
    currentIndexElement.textContent = index;
    imageSelector.value = index;
    
    // 更新提示词
    promptText.textContent = data.prompt;
    
    // 更新图片
    updateImage(normalImageContainer, `Normal/prompt_${String(index).padStart(3, '0')}_normal.jpg`, 'Normal');
    updateImage(dolaImageContainer, `Dola/prompt_${String(index).padStart(3, '0')}_standard_as_dola.jpg`, 'Dola');
    
    // 更新分数
    updateScores(normalScores, data.normal);
    updateScores(dolaScores, data.dola);
    
    // 更新导航按钮状态
    updateNavigationButtons();
}

// 更新图片显示
function updateImage(container, imagePath, type) {
    container.innerHTML = '';
    
    const img = document.createElement('img');
    img.className = 'generated-image';
    img.alt = `${type} 生成的图片`;
    img.src = imagePath;
    
    img.onload = function() {
        container.appendChild(img);
    };
    
    img.onerror = function() {
        container.innerHTML = `<div class="image-placeholder">图片加载失败<br>${imagePath}</div>`;
    };
}

// 更新分数显示
function updateScores(scoreElements, scoreData) {
    scoreElements.color.textContent = (scoreData.color_score * 100).toFixed(1) + '%';
    scoreElements.spatial.textContent = (scoreData.spatial_score * 100).toFixed(1) + '%';
    scoreElements.count.textContent = (scoreData.count_score * 100).toFixed(1) + '%';
    scoreElements.relevance.textContent = (scoreData.relevance_score * 100).toFixed(1) + '%';
    scoreElements.overall.textContent = (scoreData.overall_score * 100).toFixed(1) + '%';
    
    // 高亮最高分
    const scores = [
        { element: scoreElements.color, value: scoreData.color_score },
        { element: scoreElements.spatial, value: scoreData.spatial_score },
        { element: scoreElements.count, value: scoreData.count_score },
        { element: scoreElements.relevance, value: scoreData.relevance_score }
    ];
    
    const maxScore = Math.max(...scores.map(s => s.value));
    scores.forEach(score => {
        if (score.value === maxScore && maxScore > 0) {
            score.element.classList.add('winner');
        } else {
            score.element.classList.remove('winner');
        }
    });
}

// 更新导航按钮状态
function updateNavigationButtons() {
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    
    prevBtn.disabled = currentImageIndex <= 1;
    nextBtn.disabled = currentImageIndex >= totalImages;
}

// 显示错误信息
function showError(message) {
    normalImageContainer.innerHTML = `<div class="image-placeholder">${message}</div>`;
    dolaImageContainer.innerHTML = `<div class="image-placeholder">${message}</div>`;
    promptText.textContent = message;
}

// 导航函数
function previousImage() {
    if (currentImageIndex > 1) {
        showImage(currentImageIndex - 1);
    }
}

function nextImage() {
    if (currentImageIndex < totalImages) {
        showImage(currentImageIndex + 1);
    }
}

function goToImage() {
    const selectedIndex = parseInt(imageSelector.value);
    if (selectedIndex && selectedIndex !== currentImageIndex) {
        showImage(selectedIndex);
    }
}

// 键盘快捷键
document.addEventListener('keydown', function(e) {
    if (e.key === 'ArrowLeft') {
        previousImage();
    } else if (e.key === 'ArrowRight') {
        nextImage();
    }
});

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', initApp);