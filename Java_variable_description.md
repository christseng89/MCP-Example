# 👍 **Java** to Associate **Descriptions with Variables** Using Two Main Approaches

---

## ✅ Approach 1: Standard Javadoc Comments

```java
public class Config {

    /**
     * The tax rate applied to all purchases (e.g., 0.07 for 7%).
     */
    public static double TAX_RATE = 0.07;

    /**
     * Base URL of the API used for fetching user data.
     */
    public static String API_BASE_URL = "https://api.example.com";
}
```

**Limitations:**

- 📌 **問題 (Issue)**: Javadoc 是靜態的，無法在程式運行時由 UI 修改。
- 適合 **文件生成 (JavaDoc HTML)**，但不適合讓使用者透過 UI 更新。

---

## ✅ Approach 2: 自訂註解 (Custom Annotation) + 配置儲存

你可以用 **Java Annotation** 給變數加描述，然後透過 **反射 (Reflection)** 讀取，甚至在 UI 裡顯示/編輯。

### Step 1: 建立 Annotation (Create Annotation)

```java
import java.lang.annotation.*;

@Retention(RetentionPolicy.RUNTIME)
@Target(ElementType.FIELD)
public @interface Description {
    String value();
}
```

### Step 2: 使用 Annotation 在變數上 (Apply Annotation to Variables)

```java
public class Config {

    @Description("The tax rate applied to all purchases (e.g., 0.07 for 7%).")
    public static double TAX_RATE = 0.07;

    @Description("Base URL of the API used for fetching user data.")
    public static String API_BASE_URL = "https://api.example.com";
}
```

### Step 3: 用反射讀取描述 (Read Descriptions Using Reflection)

```java
import java.lang.reflect.Field;

public class DescriptionReader {
    public static void main(String[] args) throws Exception {
        Field[] fields = Config.class.getDeclaredFields();

        for (Field field : fields) {
            if (field.isAnnotationPresent(Description.class)) {
                Description desc = field.getAnnotation(Description.class);
                System.out.println(field.getName() + " = " + field.get(null));
                System.out.println("Description: " + desc.value());
            }
        }
    }
}
```

**Output:**

```text
TAX_RATE = 0.07
Description: The tax rate applied to all purchases (e.g., 0.07 for 7%).

API_BASE_URL = https://api.example.com
Description: Base URL of the API used for fetching user data.
```

---

## ✅ Approach 3: UI 更新流程 (UI Update Workflow Example)

1. **讀取反射資訊 (Read Reflection Info)** → 把變數名稱 + 描述 + 值，丟到 UI (例如 Swing、JavaFX、或 Web 前端)
2. **UI 編輯後 (After UI Edit)** → 使用者更新描述或值
3. **儲存更新 (Save Updates)** → 把新的描述存到資料庫、JSON 或屬性檔（而不是直接改 Annotation，因為編譯後 Annotation 是固定的）
4. **下次載入程式 (Next Program Load)** → 從外部檔案覆蓋原來的描述/值

---

## 📌 **最佳實務建議 (Best Practice Recommendations)**

- **描述 (Description)** 用 **Annotation** 定義 → 提供初始默認值
- **使用者更新 (User Updates)** 的部分 → 存在 **資料庫 / JSON / 屬性檔**，不要動到原始碼
- **載入時 (During Loading)** → 先讀 Annotation，再合併外部更新

---

## 📄 Parse a **JavaScript File** from **Java Code** and Extract Variable Information

This section explains how to extract the following from JavaScript files:

- JSDoc description
- Variable name  
- Variable value

---

## ✅ How to Do It in Java

There are two typical approaches:

---

### **Approach 1: Regex + Comment Association**

This is a simpler approach that works well for constants. Since your JS file is simple (JSDoc above const variables), you can use Java regex to capture the pattern.

```java
import java.io.*;
import java.nio.file.*;
import java.util.regex.*;
import java.util.*;

public class JsDocParser {

    public static class VariableInfo {
        String description;
        String name;
        String value;
        public String toString() {
            return String.format("Name: %s\nValue: %s\nDescription: %s\n", name, value, description);
        }
    }

    public static void main(String[] args) throws Exception {
        String jsCode = Files.readString(Path.of("sample.js"));

        // Regex: capture /** ... */ followed by const NAME = VALUE;
        Pattern pattern = Pattern.compile(
            "/\\*\\*([\\s\\S]*?)\\*/\\s*const\\s+(\\w+)\\s*=\\s*([^;]+);",
            Pattern.MULTILINE
        );

        Matcher matcher = pattern.matcher(jsCode);
        List<VariableInfo> variables = new ArrayList<>();

        while (matcher.find()) {
            VariableInfo v = new VariableInfo();
            v.description = matcher.group(1).replace("*", "").trim();
            v.name = matcher.group(2).trim();
            v.value = matcher.group(3).trim();
            variables.add(v);
        }

        // Print extracted info
        variables.forEach(System.out::println);
    }
}
```

---

#### 📌 Example Output

For your given JavaScript file:

```text
Name: TAX_RATE
Value: 0.07
Description: The tax rate applied to all purchases (e.g., 0.07 for 7%). [Reviewed]

Name: API_BASE_URL
Value: "https://api.example.com"
Description: Base URL of the API used for fetching user data. [Reviewed]
```

---

### **Approach 2: Use a Real JS Parser**

This is a more robust approach for complex JavaScript files. If your JS gets more complex, use a parser like **GraalVM**, **Nashorn (Java 8)**, or integrate a library such as **Esprima** or **Acorn** via Java. For structured parsing you can:

- Use [Rhino](https://developer.mozilla.org/en-US/docs/Mozilla/Projects/Rhino) or GraalVM's JS engine to parse AST
- Or call **comment-parser** (Node.js library) via a subprocess and let Java read JSON output

---

## 🎯 **Recommendation**

✅ For your specific need (extracting constants with comments), **Approach 1 with Regex** is the most straightforward.

---
