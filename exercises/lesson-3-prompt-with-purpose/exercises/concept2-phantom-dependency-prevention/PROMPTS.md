# Concept 2: Phantom Dependency Prevention

**Exercise Goal**: Use structured constraints to eliminate phantom dependencies before they appear.

**Prompt 1** (Structured Approach):
```xml
<task>
Optimize file processing for large CSV files (100MB to 2GB)
</task>

<context>
Python application processing customer data exports
Current implementation reads entire files into memory
Performance bottleneck during peak processing times
</context>

<requirements>
- Reduce memory usage through chunked reading
- Improve processing speed for large files
- Maintain data integrity and error handling
- Support concurrent file processing
</requirements>

<constraints>
<allowed_libraries>
- pandas (already in requirements.txt v1.5.3)
- multiprocessing (Python standard library)
- os (Python standard library)
- logging (Python standard library)
</allowed_libraries>

<forbidden_approaches>
- No external optimization libraries not listed above
- No libraries that aren't in current requirements.txt
- No experimental or beta packages
- Must show actual implementation, not just library calls
</forbidden_approaches>
</constraints>
```

**Prompt 2** (Verify Dependencies):
```xml
<task>
Generate requirements.txt for this optimized file processor
</task>

<constraints>
- Include only actual external dependencies
- Specify version constraints
- Note which imports are from standard library (no version needed)
</constraints>
```