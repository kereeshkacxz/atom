export function formatDate(isoString) {
  const date = new Date(isoString);

  const options = {
    year: "numeric",
    month: "long",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hour12: false,
  };

  return date.toLocaleString("ru-RU", options);
}

// const isoDate = "2024-08-10T20:06:12.108839Z";
// console.log(formatDate(isoDate));

export function formatDateWithoutTime(isoString) {
  const date = new Date(isoString);

  const options = {
    year: "numeric",
    month: "long",
    day: "numeric",
  };

  return date.toLocaleString("ru-RU", options);
}

// const isoDate = "2024-08-10T20:06:12.108839Z";
// console.log(formatDateWithoutTime(isoDate));

export function formatDateDigit(isoString) {
  const date = new Date(isoString);

  const hours = String(date.getHours()).padStart(2, "0"); // Часы
  const minutes = String(date.getMinutes()).padStart(2, "0"); // Минуты
  const day = String(date.getDate()).padStart(2, "0"); // День
  const month = String(date.getMonth() + 1).padStart(2, "0"); // Месяц (месяцы начинаются с 0)
  const year = date.getFullYear(); // Год

  return `${hours}:${minutes} ${day}.${month}.${year}`;
}

// const isoDate = "2024-10-10T20:30:00.000Z";
// console.log(formatDateCustom(isoDate)); // Вывод: 20:30 10.10.2024

export function getCorrectEnding(value, singular, few, plural) {
  const mod10 = value % 10;
  const mod100 = value % 100;

  if (mod10 === 1 && mod100 !== 11) {
    return singular; // год, месяц, неделя, день
  } else if (mod10 >= 2 && mod10 <= 4 && (mod100 < 12 || mod100 > 14)) {
    return few; // года, месяца, недели, дня
  } else {
    return plural; // лет, месяцев, недель, дней
  }
}

export function formatTimeDifference(milliseconds) {
  const seconds = Math.floor(milliseconds / 1000);
  const minutes = Math.floor(seconds / 60);
  const hours = Math.floor(minutes / 60);
  const days = Math.floor(hours / 24);

  const formatted = [];
  if (days > 0) {
    formatted.push(`${days} ${getCorrectEnding(days, "день", "дня", "дней")}`);
  }
  if (hours % 24 > 0) {
    formatted.push(
      `${hours % 24} ${getCorrectEnding(hours % 24, "час", "часа", "часов")}`
    );
  }
  if (minutes % 60 > 0) {
    formatted.push(
      `${minutes % 60} ${getCorrectEnding(
        minutes % 60,
        "минута",
        "минуты",
        "минут"
      )}`
    );
  }
  if (seconds % 60 > 0) {
    formatted.push(
      `${seconds % 60} ${getCorrectEnding(
        seconds % 60,
        "секунда",
        "секунды",
        "секунд"
      )}`
    );
  }

  return formatted.join(", ");
}

export function convertDatetimeLocalToGMT(datetimeLocal) {
  const localDate = new Date(datetimeLocal);

  const year = localDate.getUTCFullYear();
  const month = String(localDate.getUTCMonth() + 1).padStart(2, "0");
  const day = String(localDate.getUTCDate()).padStart(2, "0");
  const hours = String(localDate.getUTCHours()).padStart(2, "0");
  const minutes = String(localDate.getUTCMinutes()).padStart(2, "0");
  const seconds = String(localDate.getUTCSeconds()).padStart(2, "0");
  const milliseconds = String(localDate.getUTCMilliseconds()).padStart(3, "0");

  return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}.${milliseconds}Z`;
}

export function formatDateForInput(isoString) {
  const date = new Date(isoString);

  const year = date.getUTCFullYear();
  const month = String(date.getUTCMonth() + 1).padStart(2, "0");
  const day = String(date.getUTCDate()).padStart(2, "0");
  const hours = String(date.getUTCHours()).padStart(2, "0");
  const minutes = String(date.getUTCMinutes()).padStart(2, "0");

  return `${year}-${month}-${day}T${hours}:${minutes}`;
}
