export function parserName(fileName, fileContent, availableChipes) {
  const result = new Set();

  availableChipes.forEach((chip) => {
    if (fileName.includes(chip.name)) result.add(chip);
  });
  const lines = fileContent.split("\n");

  lines.forEach((line) => {
    availableChipes.forEach((chip) => {
      if (line.includes(chip.name)) result.add(chip);
    });
  });

  return Array.from(result);
}
