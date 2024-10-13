export function parserName(fileName, fileContent, availableChipes) {
  const result = new Set();

  const containsAnyPart = (text, key) => {
    const parts = key.toLowerCase().split(" ");
    return parts.some(
      (part) =>
        text.includes(part) &&
        part != "" &&
        part != "system" &&
        part != "and" &&
        part != "-"
    );
  };

  if (fileName)
    availableChipes.forEach((chip) => {
      if (containsAnyPart(fileName.toLowerCase(), chip.name)) result.add(chip);
    });
  const lines = fileContent.split("\n");

  lines.forEach((line) => {
    availableChipes.forEach((chip) => {
      if (containsAnyPart(line.toLowerCase(), chip.name)) result.add(chip);
    });
  });

  return Array.from(result);
}
