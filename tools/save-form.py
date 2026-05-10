open('tools/new-post.html', 'w').write('''<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>旅行記投稿フォーム</title>
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: Helvetica Neue, sans-serif; background: #f5f0e8; color: #3d2b1a; padding: 24px; }
h1 { font-size: 20px; margin-bottom: 24px; padding-bottom: 12px; border-bottom: 2px solid #c0392b; }
.form-group { margin-bottom: 16px; }
label { display: block; font-size: 13px; font-weight: bold; margin-bottom: 4px; color: #666; }
input, textarea, select { width: 100%; padding: 8px 10px; border: 1px solid #ccc; border-radius: 4px; font-size: 14px; font-family: inherit; background: #fff; }
textarea { resize: vertical; }
.row { display: flex; gap: 12px; }
.row .form-group { flex: 1; }
.places-wrap { display: flex; flex-direction: column; gap: 6px; }
.place-row { display: flex; gap: 8px; align-items: center; }
.place-row input { flex: 1; }
.btn-add { padding: 6px 12px; background: #e8e2d8; border: 1px solid #ccc; border-radius: 4px; cursor: pointer; font-size: 13px; }
.btn-remove { padding: 4px 8px; background: #fff; border: 1px solid #c0392b; color: #c0392b; border-radius: 4px; cursor: pointer; font-size: 12px; }
.extra-wrap { display: flex; flex-direction: column; gap: 6px; }
.extra-row { display: flex; gap: 8px; align-items: center; }
.extra-row input { flex: 1; }
.tags-input { display: flex; flex-wrap: wrap; gap: 6px; padding: 6px; border: 1px solid #ccc; border-radius: 4px; background: #fff; min-height: 38px; cursor: text; }
.tag-chip { background: #e8e2d8; padding: 2px 8px; border-radius: 12px; font-size: 13px; display: flex; align-items: center; gap: 4px; }
.tag-chip span { cursor: pointer; color: #c0392b; font-weight: bold; }
.tags-input input { border: none; outline: none; flex: 1; min-width: 80px; font-size: 14px; padding: 2px 4px; }
.btn-generate { width: 100%; padding: 12px; background: #c0392b; color: #fff; border: none; border-radius: 4px; font-size: 16px; font-weight: bold; cursor: pointer; margin-top: 8px; }
.btn-generate:hover { background: #a93226; }
.output-section { margin-top: 24px; display: none; }
.step { margin-top: 16px; }
.step h3 { font-size: 14px; margin-bottom: 6px; color: #666; }
.cmd-box { background: #1a1a1a; color: #00ff00; border-radius: 4px; padding: 12px; font-family: monospace; font-size: 13px; white-space: pre-wrap; margin-top: 8px; word-break: break-all; }
.btn-copy { margin-top: 8px; padding: 8px 16px; background: #3d2b1a; color: #fff; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; }
.hint { font-size: 12px; color: #999; margin-top: 4px; }
</style>
</head>
<body>
<h1>旅行記投稿フォーム</h1>
<div class="form-group">
  <label>タイトル *</label>
  <input type="text" id="title" placeholder="例：道東旅行2025">
</div>
<div class="row">
  <div class="form-group">
    <label>日付 *</label>
    <input type="date" id="date">
  </div>
  <div class="form-group">
    <label>旅の種類</label>
    <select id="trip_type">
      <option value="multi">複数日</option>
      <option value="day">日帰り</option>
    </select>
  </div>
  <div class="form-group">
    <label>スラッグ(URL) *</label>
    <input type="text" id="slug" placeholder="例：doto-2025">
  </div>
</div>
<div class="form-group">
  <label>場所（都道府県/自治体）*</label>
  <div class="places-wrap" id="placesWrap">
    <div class="place-row">
      <input type="text" placeholder="例：北海道/根室市">
      <button class="btn-remove" onclick="removePlace(this)">x</button>
    </div>
  </div>
  <button class="btn-add" onclick="addPlace()" style="margin-top:6px;">+ 場所を追加</button>
</div>
<div class="form-group">
  <label>タグ</label>
  <div class="tags-input" id="tagsInput" onclick="document.getElementById('tagInput').focus()">
    <input type="text" id="tagInput" placeholder="タグを入力してEnter" onkeydown="addTag(event)">
  </div>
  <p class="hint">Enterで追加</p>
</div>
<div class="form-group">
  <label>概要</label>
  <textarea id="summary" rows="2" placeholder="記事の概要を入力してください"></textarea>
</div>
<div class="form-group">
  <label>追加情報</label>
  <div class="extra-wrap" id="extraWrap">
    <div class="extra-row">
      <input type="text" placeholder="項目名（例：交通手段）" class="extra-key">
      <input type="text" placeholder="内容（例：飛行機+フェリー）" class="extra-val">
      <button class="btn-remove" onclick="removeExtra(this)">x</button>
    </div>
  </div>
  <button class="btn-add" onclick="addExtra()" style="margin-top:6px;">+ 項目を追加</button>
</div>
<div class="form-group">
  <label>本文</label>
  <textarea id="body" rows="10" placeholder="本文を入力してください。写真は ![説明](CloudinaryのURL) の形で貼り付けてください。"></textarea>
</div>
<button class="btn-generate" onclick="generate()">コマンドを生成する</button>
<div class="output-section" id="outputSection">
  <div class="step">
    <h3>① ターミナルで以下を実行してください</h3>
    <div class="cmd-box" id="cmdBox"></div>
    <button class="btn-copy" onclick="copyCmd()">コピー</button>
  </div>
  <div class="step">
    <h3>② その後、以下でpushしてください</h3>
    <div class="cmd-box">git add .
git commit -m "add new post"
git push</div>
  </div>
</div>
<script>
document.getElementById("date").value = new Date().toISOString().split("T")[0];
let tags = [];
function addTag(e) {
  if (e.key !== "Enter") return;
  const val = e.target.value.trim();
  if (!val) return;
  tags.push(val);
  const chip = document.createElement("div");
  chip.className = "tag-chip";
  chip.innerHTML = val + "<span onclick=\\"removeTag(this,\'" + val + "\')\\">x</span>";
  document.getElementById("tagsInput").insertBefore(chip, e.target);
  e.target.value = "";
}
function removeTag(el, tag) {
  tags = tags.filter(t => t !== tag);
  el.parentElement.remove();
}
function addPlace() {
  const wrap = document.getElementById("placesWrap");
  const row = document.createElement("div");
  row.className = "place-row";
  row.innerHTML = "<input type=\\"text\\" placeholder=\\"例：北海道/根室市\\"><button class=\\"btn-remove\\" onclick=\\"removePlace(this)\\">x</button>";
  wrap.appendChild(row);
}
function removePlace(btn) {
  if (document.querySelectorAll(".place-row").length > 1) btn.parentElement.remove();
}
function addExtra() {
  const wrap = document.getElementById("extraWrap");
  const row = document.createElement("div");
  row.className = "extra-row";
  row.innerHTML = "<input type=\\"text\\" placeholder=\\"項目名\\" class=\\"extra-key\\"><input type=\\"text\\" placeholder=\\"内容\\" class=\\"extra-val\\"><button class=\\"btn-remove\\" onclick=\\"removeExtra(this)\\">x</button>";
  wrap.appendChild(row);
}
function removeExtra(btn) { btn.parentElement.remove(); }
function generate() {
  const title = document.getElementById("title").value.trim();
  const date = document.getElementById("date").value;
  const slug = document.getElementById("slug").value.trim();
  const trip_type = document.getElementById("trip_type").value;
  const summary = document.getElementById("summary").value.trim();
  const body = document.getElementById("body").value.trim();
  if (!title || !date || !slug) { alert("タイトル・日付・スラッグは必須です"); return; }
  const places = [...document.querySelectorAll(".place-row input")].map(i => i.value.trim()).filter(v => v);
  const extraKeys = [...document.querySelectorAll(".extra-key")].map(i => i.value.trim());
  const extraVals = [...document.querySelectorAll(".extra-val")].map(i => i.value.trim());
  let fm = "---\\n";
  fm += "title: \\"" + title + "\\"\\n";
  fm += "date: " + date + "\\n";
  fm += "trip_type: \\"" + trip_type + "\\"\\n";
  fm += "slug: \\"" + slug + "\\"\\n";
  if (places.length) { fm += "places:\\n"; places.forEach(p => fm += "  - \\"" + p + "\\"\\n"); }
  fm += "cover: \\"\\"\\n";
  if (tags.length) { fm += "tags: [" + tags.map(t => "\\"" + t + "\\"").join(", ") + "]\\n"; }
  const extraPairs = extraKeys.map((k,i) => [k, extraVals[i]]).filter(([k]) => k);
  if (extraPairs.length) { fm += "extra:\\n"; extraPairs.forEach(([k,v]) => fm += "  " + k + ": \\"" + v + "\\"\\n"); }
  if (summary) fm += "summary: \\"" + summary + "\\"\\n";
  fm += "---\\n\\n";
  const content = fm + (body || "");
  const cmd = "cat > content/posts/" + slug + ".md << \\'MDEOF\\'\\n" + content + "\\nMDEOF";
  document.getElementById("cmdBox").textContent = cmd;
  document.getElementById("outputSection").style.display = "block";
  document.getElementById("outputSection").scrollIntoView({ behavior: "smooth" });
}
function copyCmd() {
  navigator.clipboard.writeText(document.getElementById("cmdBox").textContent).then(() => alert("コピーしました！"));
}
</script>
</body>
</html>''')
print('完了')
