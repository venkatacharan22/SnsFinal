# TruthLens AI - Enhanced Test Examples

Test the improved fact-checking system with these examples designed to showcase the enhanced Gemini prompts:

## 🔴 Fake News Examples (Should be detected as FALSE)

### Example 1: Previously Debunked NASA Claim
```
Breaking: NASA confirms Earth will experience darkness for 15 days due to planetary alignment!
```
*Expected: Should detect as debunked by Snopes/PolitiFact*

### Example 2: Sensationalized Health Misinformation
```
SHOCKING: Doctors HATE this one simple trick that cures diabetes instantly! Big Pharma doesn't want you to know this secret that has been leaked by a whistleblower!
```
*Expected: High fake confidence with multiple red flags*

### Example 3: Government Conspiracy Theory
```
Breaking: Government officials exposed in secret meeting planning to control the weather using hidden technology. Leaked documents reveal the truth they don't want you to see!
```
*Expected: Sensationalized language detection*

## ✅ Real News Examples (Should be detected as TRUE)

### Example 1: Peer-Reviewed Scientific Study
```
According to a peer-reviewed study published in Nature, scientists report new findings about climate change patterns based on 20 years of data collected from multiple research institutions.
```
*Expected: High credibility with scientific indicators*

### Example 2: Official Government Statement
```
The World Health Organization issued an official statement today regarding new guidelines for vaccine distribution. The announcement was confirmed by multiple health officials during a press conference.
```
*Expected: High credibility with official source attribution*

### Example 3: Research-Based Reporting
```
Research indicates that renewable energy adoption has increased by 15% globally this year, according to data from the International Energy Agency. The peer-reviewed report shows significant growth in solar and wind power installations.
```
*Expected: Credible with verifiable data sources*

## 🟡 Mixed/Uncertain Examples

### Example 1: Partial Information
```
Local authorities report unusual activity in the downtown area. Witnesses describe strange lights, but official confirmation is still pending investigation.
```

### Example 2: Opinion Piece
```
Many experts believe that the current economic policies may lead to significant changes in the market. However, predictions vary widely among financial analysts.
```

## 📸 Image Testing

You can also test with images by uploading:
- Screenshots of news articles
- Social media posts with news content
- Memes with news claims
- Infographics with statistics

## 🎯 Testing Tips

1. **Try different content lengths** - from short headlines to full articles
2. **Mix credible and suspicious language** to see how the AI responds
3. **Test with current events** you know the truth about
4. **Upload images** with text content to test multimodal analysis
5. **Check confidence scores** - higher scores indicate more certainty

## 🔧 API Testing

You can also test the API directly using curl:

```bash
# Test with text
curl -X POST http://localhost:3001/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"text":"Your test content here"}'

# Check service status
curl http://localhost:3001/api/status

# Health check
curl http://localhost:3001/health
```

## 📊 Understanding Results

- **isReal**: Boolean indicating if content is likely authentic
- **confidence**: Percentage score (70-95%) indicating certainty
- **reasoning**: Detailed explanation of the analysis
- **sources**: Potential sources and their credibility levels
- **redFlags**: Warning signs found in the content
- **factualClaims**: Verifiable claims identified
- **recommendation**: Suggested action for users

Remember: This is a demo system. Always verify important information through multiple reliable sources!
