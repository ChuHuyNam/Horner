const form = document.querySelector("#polynomial-form");
const inputs = [...form.querySelectorAll('input[name^="a"]')];
const xInput = document.querySelector("#x-value");
const errorMessage = document.querySelector("#form-error");

const formatNumber = (value) => {
  if (!Number.isFinite(value)) return String(value);
  if (Object.is(value, -0)) return "0";
  const rounded = Math.abs(value) < 1e-12 ? 0 : Number(value.toPrecision(12));
  return new Intl.NumberFormat("vi-VN", { maximumFractionDigits: 12, useGrouping: false }).format(rounded);
};

const mathNumber = (value) => `<mn>${formatNumber(value)}</mn>`;

function signedMathNumber(value, includeLeadingOperator = true) {
  if (!includeLeadingOperator) return mathNumber(value);
  const operator = value < 0 ? "&minus;" : "+";
  return `<mo>${operator}</mo>${mathNumber(Math.abs(value))}`;
}

function mathEquation(expression, x, result, label) {
  return `<math xmlns="http://www.w3.org/1998/Math/MathML" display="block" aria-label="${label}">
    <mstyle displaystyle="true" scriptlevel="0">
      <mrow><mi>p</mi><mo>(</mo>${mathNumber(x)}<mo>)</mo><mo>=</mo>${expression}<mo>=</mo>${mathNumber(result)}</mrow>
    </mstyle>
  </math>`;
}

function directPolynomialMath(coefficients, x, result) {
  const terms = coefficients.map((coefficient, index) => {
    const power = coefficients.length - 1 - index;
    const coefficientMarkup = signedMathNumber(coefficient, index > 0);
    if (power === 0) return coefficientMarkup;
    const variable = power === 1
      ? `<mrow><mo>(</mo>${mathNumber(x)}<mo>)</mo></mrow>`
      : `<msup><mrow><mo>(</mo>${mathNumber(x)}<mo>)</mo></mrow><mn>${power}</mn></msup>`;
    return `${coefficientMarkup}<mo>&times;</mo>${variable}`;
  }).join("");
  return mathEquation(`<mrow>${terms}</mrow>`, x, result, "Tính đa thức bằng phương pháp lặp");
}

function hornerMath(coefficients, x, result) {
  let expression = signedMathNumber(coefficients[0], false);
  for (let index = 1; index < coefficients.length; index += 1) {
    expression = `<mrow><mo>(</mo>${expression}<mo>)</mo><mo>&times;</mo>${mathNumber(x)}${signedMathNumber(coefficients[index])}</mrow>`;
  }
  return mathEquation(expression, x, result, "Biến đổi đa thức theo sơ đồ Horner");
}

function evaluateByHorner(coefficients, x) {
  let result = coefficients[0];
  const steps = [{ k: 0, coefficient: coefficients[0], calculation: `b₀ = ${formatNumber(coefficients[0])}`, result }];
  for (let k = 1; k < coefficients.length; k += 1) {
    const previous = result;
    result = previous * x + coefficients[k];
    steps.push({
      k,
      coefficient: coefficients[k],
      calculation: `${formatNumber(previous)} × ${formatNumber(x)} + ${formatNumber(coefficients[k])}`,
      result,
    });
  }
  return { result, steps };
}

function evaluateByIteration(coefficients, x) {
  let sum = 0;
  const steps = coefficients.map((coefficient, index) => {
    const power = coefficients.length - 1 - index;
    const value = coefficient * (x ** power);
    sum += value;
    return { index: index + 1, coefficient, power, value, sum };
  });
  return { result: sum, steps };
}

function render(coefficients, x) {
  const horner = evaluateByHorner(coefficients, x);
  const iteration = evaluateByIteration(coefficients, x);
  const tolerance = Number.EPSILON * Math.max(1, Math.abs(horner.result), Math.abs(iteration.result)) * 10;
  const matches = Math.abs(horner.result - iteration.result) <= tolerance;

  document.querySelector("#evaluated-label").innerHTML = `<math><mrow><mi>f</mi><mo>(</mo>${mathNumber(x)}<mo>)</mo></mrow></math>`;
  document.querySelector("#final-result").textContent = formatNumber(horner.result);
  const status = document.querySelector("#match-status");
  status.textContent = matches ? "Hai kết quả trùng khớp" : "Có sai số làm tròn";
  status.classList.toggle("mismatch", !matches);

  document.querySelector("#horner-expression").innerHTML = hornerMath(coefficients, x, horner.result);
  document.querySelector("#direct-expression").innerHTML = directPolynomialMath(coefficients, x, iteration.result);

  const coefficientCells = coefficients.map((coefficient, index) => `
    <td class="coefficient-cell"><math><msub><mi>a</mi><mn>${index + 1}</mn></msub></math><math>${signedMathNumber(coefficient, false)}</math></td>
  `).join("");
  const intermediateCells = horner.steps.slice(1).map((step, index) => {
    const intermediate = horner.steps[index].result * x;
    return `<td><math><mrow><msub><mi>c</mi><mn>${index + 1}</mn></msub><mo>=</mo>${signedMathNumber(intermediate, false)}</mrow></math></td>`;
  }).join("");
  const resultCells = horner.steps.map((step) => `
    <td><math><mrow><msub><mi>b</mi><mn>${step.k}</mn></msub><mo>=</mo>${signedMathNumber(step.result, false)}</mrow></math></td>
  `).join("");

  document.querySelector("#synthetic-steps").innerHTML = `
    <tr class="coefficient-row">${coefficientCells}<td class="synthetic-side" rowspan="2"><math><mrow><msub><mi>x</mi><mn>0</mn></msub><mo>=</mo>${signedMathNumber(x, false)}</mrow></math></td></tr>
    <tr class="intermediate-row"><td aria-label="Không có giá trị c tại bước đầu"></td>${intermediateCells}</tr>
    <tr class="result-row">${resultCells}<td class="synthetic-side"><math><mrow><mi>p</mi><mo>(</mo>${mathNumber(x)}<mo>)</mo><mo>=</mo>${signedMathNumber(horner.result, false)}</mrow></math></td></tr>
  `;
  document.querySelector("#horner-steps").innerHTML = horner.steps.map((step) => `
    <tr><td>${step.k}</td><td><math>${signedMathNumber(step.coefficient, false)}</math></td><td><math><mrow>${step.k === 0 ? `<msub><mi>b</mi><mn>0</mn></msub><mo>=</mo>${mathNumber(step.result)}` : `${mathNumber(horner.steps[step.k - 1].result)}<mo>&times;</mo>${mathNumber(x)}${signedMathNumber(step.coefficient)}`}</mrow></math></td><td><math>${signedMathNumber(step.result, false)}</math></td></tr>
  `).join("");

  document.querySelector("#iteration-steps").innerHTML = iteration.steps.map((step) => `
    <tr><td>${step.index}</td><td><math><mrow>${signedMathNumber(step.coefficient, false)}<mo>&times;</mo><msup><mrow><mo>(</mo>${mathNumber(x)}<mo>)</mo></mrow><mn>${step.power}</mn></msup></mrow></math></td><td><math>${signedMathNumber(step.value, false)}</math></td><td><math>${signedMathNumber(step.sum, false)}</math></td></tr>
  `).join("");
}

function readAndRender() {
  const coefficients = inputs.map((input) => Number(input.value));
  const x = Number(xInput.value);
  if ([...coefficients, x].some((value) => !Number.isFinite(value))) {
    errorMessage.textContent = "Vui lòng nhập đầy đủ các giá trị hợp lệ.";
    return;
  }
  errorMessage.textContent = "";
  render(coefficients, x);
}

form.addEventListener("submit", (event) => {
  event.preventDefault();
  readAndRender();
});

document.querySelector("#example-button").addEventListener("click", () => {
  [2, -3, 1, -4, 7, 8].forEach((value, index) => { inputs[index].value = value; });
  xInput.value = 2;
  readAndRender();
});

document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((item) => {
      const active = item === tab;
      item.classList.toggle("active", active);
      item.setAttribute("aria-selected", String(active));
    });
    document.querySelector("#panel-horner").hidden = tab.id !== "tab-horner";
    document.querySelector("#panel-iteration").hidden = tab.id !== "tab-iteration";
  });
});

readAndRender();

