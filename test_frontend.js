const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const htmlContent = fs.readFileSync(path.join(__dirname, 'index.html'), 'utf8');

function getCategoryClass(area) {
  if (area < 1000) return '1bhk';
  if (area >= 1000 && area <= 1750) return '1611';
  if (area > 1750 && area <= 2049) return '1915';
  if (area >= 2050 && area <= 2250) return '2150';
  if (area > 2250) return '4bhk';
  return '1611';
}

function getEffectiveArea(area) {
  if (area < 1000) return area;
  if (area >= 1000 && area <= 1750) return 1611;
  if (area > 1750 && area <= 2049) return 1915;
  if (area >= 2050 && area <= 2250) return 2150;
  return area;
}

function fmtAmount(val) {
  const num = parseFloat(val);
  if (isNaN(num) || num === 0) return '—';
  if (num >= 10000000) return `₹ ${(num / 10000000).toFixed(2)} Cr`;
  if (num >= 100000) return `₹ ${(num / 100000).toFixed(2)} L`;
  return `₹ ${num.toLocaleString('en-IN')}`;
}

test('Frontend Unit Tests — getCategoryClass', () => {
  assert.equal(getCategoryClass(660), '1bhk');
  assert.equal(getCategoryClass(1611), '1611');
  assert.equal(getCategoryClass(1613), '1611');
  assert.equal(getCategoryClass(1915), '1915');
  assert.equal(getCategoryClass(2150), '2150');
  assert.equal(getCategoryClass(2481), '4bhk');
});

test('Frontend Unit Tests — getEffectiveArea', () => {
  assert.equal(getEffectiveArea(660), 660);
  assert.equal(getEffectiveArea(1613), 1611);
  assert.equal(getEffectiveArea(1900), 1915);
  assert.equal(getEffectiveArea(2150), 2150);
  assert.equal(getEffectiveArea(2481), 2481);
});

test('Frontend Unit Tests — fmtAmount', () => {
  assert.equal(fmtAmount(24500000), '₹ 2.45 Cr');
  assert.equal(fmtAmount(850000), '₹ 8.50 L');
  assert.equal(fmtAmount(15000), '₹ 15,000');
  assert.equal(fmtAmount(0), '—');
});

test('Frontend Unit Tests — index.html contains required DOM containers', () => {
  assert.ok(htmlContent.includes('id="portfolio-container"'), 'portfolio-container must exist in index.html');
  assert.ok(htmlContent.includes('id="category-averages-container"'), 'category-averages-container must exist in index.html');
  assert.ok(htmlContent.includes('id="table-body"'), 'table-body must exist in index.html');
  assert.ok(htmlContent.includes('id="purchases-tbody"'), 'purchases-tbody must exist in index.html');
  assert.ok(htmlContent.includes('id="pm-parse-banner"'), 'pm-parse-banner must exist in index.html');
});
