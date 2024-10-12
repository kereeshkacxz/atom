export function parserName(fileName, fileContent, availableChipes) {
  const result = new Set();
  if (fileName)
    availableChipes.forEach((chip) => {
      if (fileName.toLowerCase().includes(chip.name.toLowerCase()))
        result.add(chip);
    });
  const lines = fileContent.split("\n");

  lines.forEach((line) => {
    availableChipes.forEach((chip) => {
      if (line.toLowerCase().includes(chip.name.toLowerCase()))
        result.add(chip);
    });
  });

  return Array.from(result);
}
